import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3301",
    "http://localhost",
    "http://localhost:3300",

]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Import scheduler.py so we can modify the scheduler
from scheduler import app as app_rocketry

session = app_rocketry.session


def load_data(file):
    cache_data = joblib.load("data/"+file)
    return cache_data


@app.get("/actual_data")
async def actual_data(file: str ="data"):
    return load_data(file)

@app.get("/raw_data")
async def raw_data(file: str ="raw_data"):
    return load_data(file)

@app.get("/tasks")
async def read_tasks():
    return list(session.tasks)


@app.get("/logs")
async def read_logs():
    "Get task logs"
    repo = session.get_repo()
    return repo.filter_by().all()
