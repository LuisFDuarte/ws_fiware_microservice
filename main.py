import asyncio
import logging
import uvicorn
import os
from api import app as app_fastapi
from scheduler import app as app_rocketry

# Load the environment variables from the keys.env file
# load_dotenv("keys.env")

# Get the port from the environment variable
PORT = int(os.getenv('PORT'))
print(PORT)

class Server(uvicorn.Server):
    """
    Customized uvicorn.Server
    Uvicorn server overrides signals and we need to include
    Rocketry to the signals.
    """
    def handle_exit(self, sig: int, frame) -> None:
        """
        Handle the exit signal by shutting down the session
        before calling the parent's handle_exit method.
        """
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    """
    Run Rocketry and FastAPI
    """
    # Create an instance of the Server class
    server = Server(config=uvicorn.Config(app_fastapi, workers=1, loop="asyncio", host="0.0.0.0", port=PORT))
    print(app_fastapi)

    # Run the server.serve() and app_rocketry.serve() as async tasks
    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(app_rocketry.serve())

    # Wait for both tasks to complete
    await asyncio.wait([sched, api])


if __name__ == "__main__":
    # Print Rocketry's logs to terminal
    logger = logging.getLogger("rocketry.task")
    logger.addHandler(logging.StreamHandler())

    # Run both applications
    asyncio.run(main())