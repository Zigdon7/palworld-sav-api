"""This module handles environment variables and configuration files."""

from functools import lru_cache
from typing import Any, Dict, Tuple

import yaml  # type: ignore
from pydantic import BaseModel, model_validator
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from logging_config import LoggerManager

logger = LoggerManager()


class AppConfig(BaseModel):
    """App configuration."""

    title: str
    description: str
    version: str
    docs_url: str
    root_path: str
    environment: str

# class ApIConfig(BaseModel):
#     """Api keys"""
#     open_ai: str

class DBConfig(BaseModel):
    """Database configuration settings."""

    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    echo_sql: bool = False
    db_url: str

    @model_validator(mode="before")
    def create_db_url(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Create the database url."""
        db_user = values.get("db_user")
        db_password = values.get("db_password")
        db_host = values.get("db_host")
        db_port = values.get("db_port")
        db_name = values.get("db_name")

        if db_user and db_password and db_host and db_port and db_name:
            values[
                "db_url"
            ] = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        return values


class LogConfig(BaseModel):
    """Logging configuration."""

    level: str

def merge_dicts(dict_list: list[dict]) -> dict:
    """Merge a list of dictionaries into one."""
    merged_dict = {}
    for d in dict_list:
        merged_dict.update(d)
    return merged_dict


class YamlSettingsSource(PydanticBaseSettingsSource):
    """Load settings from a yaml file."""

    def __init__(self, settings_cls: type[BaseSettings]):
        features_file = "./config.yaml"
        with open(features_file, "r") as stream:  # pylint: disable=W1514
            self.features = yaml.safe_load(stream)
        super().__init__(settings_cls)

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        field_value = self.features.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = merge_dicts(field_value)

        return d


class Config(BaseSettings):
    """Config class."""

    app: AppConfig
    db: DBConfig
    log: LogConfig
    # api_keys: ApIConfig
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    @classmethod
    def settings_customise_sources(  # pylint: disable=R0913
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Define the sources and their order for loading the settings values."""
        return (
            init_settings,
            env_settings,
            YamlSettingsSource(settings_cls),
            file_secret_settings,
        )


@lru_cache()
def get_config() -> Config:
    """Get the configuration."""
    return Config()  # type: ignore


config = get_config()
