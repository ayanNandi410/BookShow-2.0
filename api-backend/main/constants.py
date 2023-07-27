import os
BASE_URL = "http://127.0.0.1:5000"

baseDir = os.path.abspath(os.getcwd())
SQLITE_DB_DIR = os.path.join(baseDir, "./dbDir")
DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "ticketdb.sqlite")
