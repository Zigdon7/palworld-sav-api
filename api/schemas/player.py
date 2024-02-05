import uuid
from typing import List, Dict, Optional

class Vector4:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

class IndividualId:
    def __init__(self, player_uid: uuid.UUID, instance_id: uuid.UUID):
        self.player_uid = player_uid
        self.instance_id = instance_id

class LastTransform:
    def __init__(self, rotation: Vector4, translation: Vector3):
        self.rotation = rotation
        self.translation = translation

class Color:
    def __init__(self, r: float, g: float, b: float, a: float):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

class PlayerCharacterMakeData:
    def __init__(self, body_mesh_name: str, head_mesh_name: str, hair_mesh_name: str, arm_volume: float, torso_volume: float, leg_volume: float, hair_color: Color, brow_color: Color, body_color: Color, body_subsurface_color: Color, eye_color: Color, eye_material_name: str, voice_id: int):
        self.body_mesh_name = body_mesh_name
        self.head_mesh_name = head_mesh_name
        self.hair_mesh_name = hair_mesh_name
        self.arm_volume = arm_volume
        self.torso_volume = torso_volume
        self.leg_volume = leg_volume
        self.hair_color = hair_color
        self.brow_color = brow_color
        self.body_color = body_color
        self.body_subsurface_color = body_subsurface_color
        self.eye_color = eye_color
        self.eye_material_name = eye_material_name
        self.voice_id = voice_id

class ContainerId:
    def __init__(self, id: uuid.UUID):
        self.id = id

class InventoryInfo:
    def __init__(self, common_container_id: ContainerId, drop_slot_container_id: ContainerId, essential_container_id: ContainerId, weapon_load_out_container_id: ContainerId, player_equip_armor_container_id: ContainerId, food_equip_container_id: ContainerId):
        self.common_container_id = common_container_id
        self.drop_slot_container_id = drop_slot_container_id
        self.essential_container_id = essential_container_id
        self.weapon_load_out_container_id = weapon_load_out_container_id
        self.player_equip_armor_container_id = player_equip_armor_container_id
        self.food_equip_container_id = food_equip_container_id

class KeyValue:
    def __init__(self, key: str, value: bool):
        self.key = key
        self.value = value

class RecordData:
    def __init__(self, tower_boss_defeat_flag: List[KeyValue], normal_boss_defeat_flag: List[KeyValue], tribe_capture_count: int, pal_capture_count: List[KeyValue], paldeck_unlock_flag: List[KeyValue], pal_capture_count_bonus_count_tier1: int, pal_capture_count_bonus_count_tier2: int, pal_capture_count_bonus_count_tier3: int, relic_obtain_for_instance_flag: List[KeyValue], relic_possess_num: int, note_obtain_for_instance_flag: List[KeyValue], fast_travel_point_unlock_flag: List[KeyValue]):
        self.tower_boss_defeat_flag = tower_boss_defeat_flag
        self.normal_boss_defeat_flag = normal_boss_defeat_flag
        self.tribe_capture_count = tribe_capture_count
        self.pal_capture_count = pal_capture_count
        self.paldeck_unlock_flag = paldeck_unlock_flag
        self.pal_capture_count_bonus_count_tier1 = pal_capture_count_bonus_count_tier1
        self.pal_capture_count_bonus_count_tier2 = pal_capture_count_bonus_count_tier2
        self.pal_capture_count_bonus_count_tier3 = pal_capture_count_bonus_count_tier3
        self.relic_obtain_for_instance_flag = relic_obtain_for_instance_flag
        self.relic_possess_num = relic_possess_num
        self.note_obtain_for_instance_flag = note_obtain_for_instance_flag
        self.fast_travel_point_unlock_flag = fast_travel_point_unlock_flag

class Player:
    def __init__(self, version: int, timestamp: int, player_uid: uuid.UUID, individual_id: IndividualId, last_transform: LastTransform, player_character_make_data: PlayerCharacterMakeData, otomo_character_container_id: ContainerId, inventory_info: InventoryInfo, technology_point: int, boss_technology_point: int, unlocked_recipe_technology_names: Dict[str, List[str]], pal_storage_container_id: ContainerId, record_data: RecordData, is_selected_init_map_point: bool):
        self.version = version
        self.timestamp = timestamp
        self.player_uid = player_uid
        self.individual_id = individual_id
        self.last_transform = last_transform
        self.player_character_make_data = player_character_make_data
        self.otomo_character_container_id = otomo_character_container_id
        self.inventory_info = inventory_info
        self.technology_point = technology_point
        self.boss_technology_point = boss_technology_point
        self.unlocked_recipe_technology_names = unlocked_recipe_technology_names
        self.pal_storage_container_id = pal_storage_container_id
        self.record_data = record_data
        self.is_selected_init_map_point = is_selected_init_map_point