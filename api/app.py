import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi_router_controller import Controller, ControllersTags
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api import controllers
from api.config import config
# from api.database.database import sessionmanager
from logging_config import LoggerManager

logger = LoggerManager()

@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=W0621, W0613
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    # if sessionmanager._engine is not None:  # pylint: disable=W0212
    #     # Close the DB connection
    #     await sessionmanager.close()
    #     logger.info("Database connection closed.")


app: FastAPI = FastAPI(
    title=config.app.title,
    description=config.app.description,
    version=config.app.version,
    docs_url=config.app.docs_url,
    openapi_tags=ControllersTags,
    root_path=config.app.root_path,
    listeners=lifespan,
)

origins = [
    "http://localhost:3000",  # React
    "http://localhost:8001",  # FastAPI server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


controllers.load_controllers()
for router in Controller.routers():
    app.include_router(router)
    logger.info(f"Registered router prefix: {router.prefix}")
