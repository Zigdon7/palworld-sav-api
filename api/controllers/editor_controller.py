from fastapi import APIRouter, Depends, status
from fastapi_router_controller import Controller
from api.services.editor import EditorService
from api.schemas.error import ErrorResponse 
from logging_config import LoggerManager

logger = LoggerManager()
router = APIRouter(prefix="/editor")
controller = Controller(router, openapi_tag={"name": "editor-controller"})

@controller.use()
@controller.resource()
class EditorController:
    """Editor Controller class."""

    def __init__(
        self,  # noqa: ANN101
    ) -> None:
        """Initialize EditorController."""
        self.service = EditorService()

    @controller.route.get(
        "/values/{filename}",
        tags=["editor-controller"],
        summary="Get all values from a .sav file",
        status_code=status.HTTP_200_OK,
        response_description="Values retrieved",
        responses={
            status.HTTP_404_NOT_FOUND: {
                "model": ErrorResponse,
                "description": "File not found",
            },
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "model": ErrorResponse,
                "description": "Internal Server Error",
            },
        },
    )
    async def get_values(self, filename: str) -> dict:
        """Get all values from a .sav file."""
        values = await self.service.get_all_values(filename)
        return {"values": values}

    @controller.route.get(
        "/simplify/{filename}",
        tags=["editor-controller"],
        summary="Generate a flattened JSON file",
        status_code=status.HTTP_200_OK,
        response_description="Flattened JSON file generated",
        responses={
            status.HTTP_404_NOT_FOUND: {
                "model": ErrorResponse,
                "description": "File not found",
            },
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "model": ErrorResponse,
                "description": "Internal Server Error",
            },
        },
    )
    
    async def generate_simplified_json(self, filename: str) -> dict:
        """Generate a flattened JSON file."""
        simplified_json = await self.service.simplify_json_file(filename)
        return {"flattened_json": simplified_json}
    
    @controller.route.get(
        "/find-value/{filename}/{id_value}",
        tags=["editor-controller"],
        summary="Find a value in a JSON file",
        status_code=status.HTTP_200_OK,
        response_description="Value found",
        responses={
            status.HTTP_404_NOT_FOUND: {
                "model": ErrorResponse,
                "description": "File not found",
            },
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "model": ErrorResponse,
                "description": "Internal Server Error",
            },
        },
    )
    async def find_value_route(self, filename: str, id_value: str) -> dict:
        """Find a value in a JSON file."""
        result = await self.service.find_value(filename, id_value)
        return {"result": result}