""" """

import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

class DBConfig(object):
    """Configs for the database"""

    SQLALCHEMY_DATABASE_URI = (
        os.getenv("SQLALCHEMY_DATABASE_URI") or "sqlite:///ringstech.db"
    )
