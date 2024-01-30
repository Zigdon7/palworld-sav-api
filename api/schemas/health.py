"""Module for health schemas."""

from enum import Enum
from pydantic import BaseModel


class Health(Enum):
    """Creates the health enum."""

    HEALTHY = "healthy"


class HealthResponse(BaseModel):
    """Health Status attributes model."""

    status: Health 

    class Config:
        """Config for HealthResponse."""

        schema_extra = {
            "example": {
                "status": "healthy",
            }
        }