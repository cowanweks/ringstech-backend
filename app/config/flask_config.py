from cachelib.file import FileSystemCache
from app.config import DBConfig


class Config(DBConfig):
    PORT = 3000
    DEBUG = True
    TESTING = False
    HOST = "0.0.0.0"

    # Session settings
    # SESSION_TYPE = "cachelib"
    # SESSION_USE_SIGNER = True
    # SESSION_SERIALIZATION_FORMAT = "json"
    # SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir="sessions")

    APP_NAME = "RingsTech"


class DevelopmentConfig(Config):
    ENV = "development"
    pass


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    ENV = "testing"
    TESTING = True


class ProductionConfig(Config):
    PORT = 3001
    ENV = "production"
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://uh9fv8g0lgees:p01d87a2b1e59c66492e1766729784601b185b417509eaca2710ad3e1c7e67c41@cd1goc44htrmfn.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d5hu634qnferhg"
