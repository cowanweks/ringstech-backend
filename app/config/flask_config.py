import secrets
from cachelib.file import FileSystemCache
from app.config import DBConfig


class Config(DBConfig):
    PORT = 3000
    DEBUG = True
    TESTING = False
    HOST = "127.0.0.1" or "localhost"
    SECRET_KEY = secrets.token_hex(16)

    # Session settings
    SESSION_TYPE = "cachelib"
    SESSION_USE_SIGNER = True
    SESSION_SERIALIZATION_FORMAT = "json"
    SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir="sessions")

    APP_NAME = "RingsTech"


class DevelopmentConfig(Config):
    ENV = "development"
    pass


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True


class ProductionConfig(Config):
    PORT = 3001
    ENV = "production"
    DEBUG = False
    HOST = "0.0.0.0"
    TESTING = True
