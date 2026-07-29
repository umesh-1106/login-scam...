import os

class Config:
    # Flask Secret Key
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")

    # MySQL Configuration
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB = os.environ.get("MYSQL_DB", "attendance_system")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))

    # Session Configuration
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
