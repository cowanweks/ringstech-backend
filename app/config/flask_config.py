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
    SQLALCHEMY_DATABASE_URI = "postgresql://u5dvnv50squoju:p2e7f670526dca923dfccd2b19fe826939ae94a5d6ddbd0bc22495f3adb5006b3@c5hilnj7pn10vb.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6h6o8s21fhl84"