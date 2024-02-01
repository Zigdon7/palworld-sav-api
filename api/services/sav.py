import aiofiles
import json
from api.core.palsav import decompress_sav_to_gvas
from api.core.gvas import GvasFile
from api.core.paltypes import PALWORLD_CUSTOM_PROPERTIES, PALWORLD_TYPE_HINTS
from api.core.noindent import CustomEncoder
from logging_config import LoggerManager

logger = LoggerManager()

class SavService:
    def __init__(self):
        pass
    
    def flatten_json(self, y):
        out = {}

        def flatten(x, name=''):
            if isinstance(x, dict):
                for a in x:
                    flatten(x[a], name + a + '_')
            elif isinstance(x, list):
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return out
    
    def simplify_json(self, data):
        if isinstance(data, dict):
            if 'value' in data and 'type' in data:
                return self.simplify_json(data['value'])
            else:
                return {key: self.simplify_json(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.simplify_json(element) for element in data]
        else:
            return data

    async def flatten_json_file(self, filename: str):
        output_filename = filename.replace('.json', '') + '-flattened.json'

        with open(f"/app/outputs/{filename}", 'r') as file:
            data = json.load(file)

            if 'properties' in data:
                flattened_data = self.simplify_json(data['properties'])
            else:
                first_key = next(iter(data))
                flattened_data = self.simplify_json(data)

        with open(f"/app/outputs/{output_filename}", 'w') as file:
            json.dump(flattened_data, file, indent=4)

        return True

    async def get_all_values(self, filename: str):
        with open(f"/app/outputs/{filename}.json", 'r') as file:
            data = json.load(file)
            values = data.get('values', [])
            keys = [list(item.keys()) for item in values if isinstance(item, dict)]
        return keys
    
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
    
    async def find_value(self, filename: str, id_value: str):
        async with aiofiles.open(f"/app/outputs/{filename}.json", 'r') as file:
            data = await file.read()
            data = json.loads(data)
            return self.find_id_in_dict(data, id_value)

    def find_id_in_dict(self, data, id_value, parent=None):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'ID' and value == id_value:
                    logger.info(f"ID: {value}")
                    return parent
                if isinstance(value, (dict, list)):
                    result = self.find_id_in_dict(value, id_value, data)
                    if result:
                        return result
        elif isinstance(data, list):
            for item in data:
                result = self.find_id_in_dict(item, id_value, data)
                if result:
                    return result
        return None
    
    def chunk_properties(self, properties: dict, chunk_size: int = 1):
        items = list(properties["worldSaveData"]["value"].items())
        logger.info("Length of properties: " + str(len(items)))
        for i in range(0, len(items), chunk_size):
            yield dict(items[i:i + chunk_size])

 