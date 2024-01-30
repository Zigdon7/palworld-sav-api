from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi_router_controller import Controller
# from sqlalchemy.ext.asyncio import AsyncSession
# from api.database.database import get_db_session
from api.services.sav import SavService
from api.schemas.error import ErrorResponse 
from logging_config import LoggerManager

logger = LoggerManager()
router = APIRouter(prefix="/sav")
controller = Controller(router, openapi_tag={"name": "sav-controller"})

@controller.use()
@controller.resource()
class SavController:
    """Sav Controller class."""

    def __init__(
        self,  # noqa: ANN101
        # db_session: AsyncSession = Depends(get_db_session),
    ) -> None:
        """Initialize SavController."""
        self.service = SavService()

    @controller.route.post(
        "/upload",
        tags=["sav-controller"],
        summary="Upload a .sav file",
        status_code=status.HTTP_201_CREATED,
        response_description="File uploaded",
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "model": ErrorResponse,
                "description": "Internal Server Error",
            },
        },
    )
    async def upload_file(self, file: UploadFile = File(...)) -> dict:
        """Upload a .sav file."""
        logger.info(f"Received file: {file.filename}")
        
        if file.filename.endswith('.sav'):
            file_bytes = await file.read()  # read the file into bytes
            json = await self.service.decompress_sav(file_bytes, file.filename)  # decompress the .sav file
            return {"message": json}
        else:
            return {"message": False, "error": "Invalid file type. Please upload a .sav file."}