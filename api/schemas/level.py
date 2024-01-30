"""Module for error schemas."""
from typing import Any
from datetime import datetime 
from pydantic import BaseModel 


class Level(BaseModel):
    """Level model."""

    MapObjectSaveData: Any
    FoliageGridSaveDataMap : Any
    MapObjectSpawnerInStageSaveData: Any
    WorkSaveData: Any
    BaseCampSaveData: Any
    DynamicItemSaveData: Any
    CharacterContainerSaveData: Any
    GroupSaveDataMap: Any
    ItemContainerSaveData : Any
    CharacterParameterStorageSaveData:Any
    GameTimeSaveData: Any
    EnemyCampSaveData : Any
    DungeonPointMarkerSaveData: Any
    DungeonSaveData : Any