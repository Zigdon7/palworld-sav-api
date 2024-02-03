# //service to manage calls to edit the json files or aggragate data
# //remove item calls
# //remove mon calls
# //add item
# //add mon
# //maybe validation for types of item and mons
import aiofiles
import json
from logging_config import LoggerManager

logger = LoggerManager()

class EditorService:
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

    async def simplify_json_file(self, filename: str):
        output_filename = filename.replace('.json', '') + '-simplified.json'

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