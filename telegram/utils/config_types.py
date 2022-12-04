import configparser
import typing
from dataclasses import dataclass


@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379
    db: typing.Optional[int] = None
    password: typing.Optional[str] = None
    prefix: str = "fsm"

    def __post_init__(self):
        self.port = int(self.port)
        self.db = self.db and int(self.db)


@dataclass
class SQLConfig:
    user: str = ""
    password: str = ""
    database: str = ""
    driver: str = "mysql + aiomysql"
    host: str = "localhost"
    special: str = "charset = utf8mb4"

    def __post_init__(self):
        self.sql_url = (f"{self.driver}://{self.user}:{self.password}@{self.host}/"
                        f"{self.database}?{self.special}")


@dataclass
class Config:
    bot_token: str
    admin_id: int
    sql_conf: SQLConfig = None
    redis_conf: RedisConfig = None

    def __post_init__(self):
        self.admin_id = int(self.admin_id)


def readconfig(file="global_settings.ini") -> Config:
    bot_data = configparser.ConfigParser(allow_no_value=True)
    bot_data.read(file)

    redis = bot_data.has_section('redis') and RedisConfig(**bot_data['redis'])
    sql = bot_data.has_section('sql_db') and SQLConfig(**bot_data['sql_db'])
    config: Config = Config(
        **bot_data['tg_bot'],
        sql_conf=sql,
        redis_conf=redis,
    )
    return config
