def json_to_player(json_string: str) -> Player:
        data = json.loads(json_string)

        individual_id = IndividualId(
            player_uid=UUID(data['individual_id']['player_uid']),
            instance_id=UUID(data['individual_id']['instance_id'])
        )

        last_transform = LastTransform(
            rotation=Vector4(*data['last_transform']['rotation']),
            translation=Vector3(*data['last_transform']['translation'])
        )

        player_character_make_data = PlayerCharacterMakeData(**data['player_character_make_data'])

        otomo_character_container_id = ContainerId(id=UUID(data['otomo_character_container_id']['id']))

        inventory_info = InventoryInfo(**data['inventory_info'])

        record_data = RecordData(**data['record_data'])

        player = Player(
            version=data['version'],
            timestamp=data['timestamp'],
            player_uid=UUID(data['player_uid']),
            individual_id=individual_id,
            last_transform=last_transform,
            player_character_make_data=player_character_make_data,
            otomo_character_container_id=otomo_character_container_id,
            inventory_info=inventory_info,
            technology_point=data['technology_point'],
            boss_technology_point=data['boss_technology_point'],
            unlocked_recipe_technology_names=data['unlocked_recipe_technology_names'],
            pal_storage_container_id=ContainerId(id=UUID(data['pal_storage_container_id']['id'])),
            record_data=record_data,
            is_selected_init_map_point=data['is_selected_init_map_point']
        )

        return player