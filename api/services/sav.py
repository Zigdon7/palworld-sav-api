import aiofiles
import json
from api.core.palsav import decompress_sav_to_gvas
from api.core.gvas import GvasFile
from api.core.paltypes import PALWORLD_CUSTOM_PROPERTIES, PALWORLD_TYPE_HINTS
from api.core.json_tools import CustomEncoder
from logging_config import LoggerManager

logger = LoggerManager()

class SavService:
    def __init__(self):
        pass
    async def decompress_sav(self, sav_data: bytes, filename: str, output_path: str = '/app/outputs/', minify: bool = False) -> bool:
        raw_gvas, _ = decompress_sav_to_gvas(sav_data)
        logger.info("Loading GVAS file")
        gvas_file = GvasFile.read(raw_gvas, PALWORLD_TYPE_HINTS, PALWORLD_CUSTOM_PROPERTIES)
        logger.info("Splitting JSON")
        properties = gvas_file.properties
        filename.replace('.sav', '')
        if filename.startswith("Level"):
            for index, chunk in enumerate(self.chunk_properties(properties)):
                keys = list(chunk.keys())
                keys_string = '-'.join(keys)
                print(f"Writing JSON chunk to {output_path}{filename}-{keys_string}.json")
                async with aiofiles.open(f"{output_path}{filename}-{keys_string}.json", mode='w', encoding="utf8") as f:
                    indent = None if minify else "\t"
                    await f.write(json.dumps(chunk, indent=indent, cls=CustomEncoder))
        else:
            print(f"Writing JSON to {output_path}{filename}.json")
        
            async with aiofiles.open(f"{output_path}{filename}.json", mode='w', encoding="utf8") as f:
                indent = None if minify else "\t"
                await f.write(json.dumps(gvas_file.dump(), indent=indent, cls=CustomEncoder))
        
        return True
    
    def chunk_properties(self, properties: dict, chunk_size: int = 1):
        items = list(properties["worldSaveData"]["value"].items())
        logger.info("Length of properties: " + str(len(items)))
        for i in range(0, len(items), chunk_size):
            yield dict(items[i:i + chunk_size])

 