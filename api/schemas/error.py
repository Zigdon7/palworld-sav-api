"""Module for error schemas."""

from typing import Optional
from datetime import datetime 
from fastapi import status
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel 


class ErrorDetails(BaseModel):
    """Creates the error object for errordetails prop"""

    timestamp: datetime = datetime.now()
    status_code: Optional[int] = status.HTTP_500_INTERNAL_SERVER_ERROR
    exeption: str
    description: str


class ErrorResponse(ErrorDetails):
    """Creates the error object for error prop"""

    error: ErrorDetails