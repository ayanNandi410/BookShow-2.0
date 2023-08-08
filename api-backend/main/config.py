import os
import secrets, string, secrets
baseDir = os.path.abspath(os.getcwd())


class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"


class LocalDevConfig():
    SQLITE_DB_DIR = os.path.join(baseDir, "./dbDir")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(SQLITE_DB_DIR, "ticketdb.sqlite")
    SECRET_KEY = secrets.token_urlsafe(26)
    SECURITY_PASSWORD_SALT = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for i in range(32))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_TRACKABLE = True
    SECURITY_USERNAME_ENABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False

    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379

