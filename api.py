import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# List of allowed origins for CORS
origins = [
    "http://localhost:3301",
    "http://localhost",
    "http://localhost:3300",
]

app = FastAPI()

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import scheduler.py so we can access the session object
from scheduler import app as app_rocketry

# Create a session object
session = app_rocketry.session


def load_data(file: str) -> dict:
    """
    Load data from the specified file in the data directory.
    """
    cache_data = joblib.load("data/" + file)
    return cache_data


@app.get("/actual_data")
async def actual_data(file: str = "data"):
    """
    Return the actual data for the specified file.
    """
    return load_data(file)


@app.get("/raw_data")
async def raw_data(file: str = "raw_data"):
    """
    Return the raw data for the specified file.
    """
    return load_data(file)


@app.get("/tasks")
async def read_tasks():
    """
    Return a list of all tasks in the scheduler session.
    """
    return list(session.tasks)


@app.get("/logs")
async def read_logs():
    """
    Return the logs for all tasks in the scheduler session.
    """
    repo = session.get_repo()
    return repo.filter_by().all()