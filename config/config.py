import logging
import os
from dataclasses import dataclass

from environs import Env

logger = logging.getLogger(__name__)

@dataclass
class BotSettings:
    token: str

@dataclass
class LogSettings:
    level: str
    format: str

@dataclass
class Config:
    bot: BotSettings
    log: LogSettings

def load_config(path: str | None = None) -> Config:
    env = Env()

    if path:
        if not os.path.exists(path):
            logger.warning(".env file not found at '%s', skipping...", path)
        else:
            logger.info("Loading .env from '%s'", path)

    env.read_env(path)

    return Config(
        bot=BotSettings(token=env("BOT_TOKEN")),
        log=LogSettings(level=env("LOG_LEVEL"), format=env("LOG_FORMAT"))

    )