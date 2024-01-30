"""Controllers package initializer."""
from pathlib import Path

from fastapi_router_controller import ControllerLoader

def load_controllers() -> None:
    """Load controllers."""
    ControllerLoader.load(
        Path(__file__).parent.as_posix(),
        __package__,
    )