from rocketry import Rocketry
from rocketry.conds import every, after_success
import requests
from requests.exceptions import HTTPError
from requests.exceptions import Timeout
import joblib
from dotenv import load_dotenv
import os
import time
import json

# Loading environment variables from keys.env file
load_dotenv("keys.env")

# Setting the environment variables
APP_KEY = str(os.getenv("APP_KEY"))
API_KEY = str(os.getenv("API_KEY"))
SERVER = str(os.getenv("SERVER")) # 200.3.144.214 10.61.3.135
ID = str(os.getenv("ID"))

def get_meteorological_data():
    """
    Retrieve the meteorological data from the API.
    """
    url = "https://api.ambientweather.net/v1/devices?apiKey={}&applicationKey={}".format(API_KEY, APP_KEY)

    try:
        # Send a GET request
        response = requests.request("GET", url, timeout=3)
        # Raise exception for non-200 status codes
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Timeout as err:
        print(f"The request timed out: {err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        # If the request is successful
        data = response.json()
        data_processed = convert_units(data[0]['lastData'])
        joblib.dump(data_processed, "data/data")
        joblib.dump(data[0]['lastData'], "data/raw_data")

def convert_units(data):
    """Convert the unit of the provided data and return the processed data.

    Args:
    data (dict): A dictionary of key-value pairs where the key is the name of the data and the value is the data's value.

    Returns:
    dict: A dictionary of key-value pairs where the key is the name of the processed data and the value is the processed data's value.

    """
    processed_data={}
    for key, value in data.items():
        if key == "tempf":
            processed_data["Temperature"] = (value - 32) * (5/9) # F to C
        elif key == "humidity":
            processed_data["Humidity"] = value
        elif key == "humidityin":
            processed_data["Humidity_inside"] = value
        elif key == "tempinf":
            processed_data["Temperature_inside"] = (value - 32) * (5/9) # F to C
        elif key == "windspeedmph":
            processed_data["Wind_speed"] = value * 0.44704 # mph to m/s
        elif key == "winddir":
            processed_data["Wind_direction"] = value
        elif key == "dateutc":
             processed_data["Timestamp"] = value
        elif key == "uv":
            processed_data["UV"] = value
        elif key == "solarradiation":
            processed_data["Solar_radiation"] = value
        elif key == "hourlyrainin":
            processed_data["Hourly_rain"] = value*25.4 # inch to mm
        elif key == "baromrelin":
            processed_data["Pressure"] = value*25.4 # inch to mm
        elif key == "soilhum1":
            processed_data["Soil_humidity"] = value
        elif key == "pm10_in_aqin":
            processed_data["PM_10"] = value
        elif key == "pm_in_temp_aqin":
            processed_data["Temperature_AQIN"] = (value - 32) * (5/9) # F to C
        elif key == "pm_in_humidity_aqin":
            processed_data["Humidity_AQIN"] = value
        elif key == "aqi_pm25_aqin":
            processed_data["AQI_PM_2_5"] = value
        elif key == "pm25_in_aqin":
            processed_data["PM_2_5"] = value
        elif key == "co2_in_aqin":
            processed_data["CO2"] = value
    return processed_data

def process_data():
    """Load data from the file and pass it to the request_to_fiware function."""
    processed_data = {}
    processed_data = joblib.load("data/data")
    request_to_fiware(processed_data)


def request_to_fiware(data):
    """Make a POST request to FIWARE server with the provided data and headers.

    Handle any errors that may occur during the request.
    """
    url = "http://"+SERVER+":1026/v2/entities/"+ID+"/attrs"

    payload = {}
    for key, value in data.items():
        payload[key] = {
            "type": "Number",
            "value": value,
        }
    headers = {'Content-Type': 'application/json'}
    print("url", url)
    print("headers", headers)
    print(json.dumps(payload, indent=4))

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=3)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Timeout as err:
        print(f"The request timed out: {err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        data = response  # .json()
        print(data)
    time.sleep(0.3)


@app.task("every 45 seconds")
async def get_weather_station_data():
    """Retrieve meteorological data."""
    get_meteorological_data()

@app.task("every 1 minute")
async def send_data_to_fiware():
    """Process the data and send it to the specified server."""
    process_data()

if __name__ == "__main__":
    # If this script is run, only Rocketry is run
    app.run()