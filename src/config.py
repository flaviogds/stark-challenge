import base64
import json
from os import environ

from dotenv import load_dotenv

load_dotenv(".env")


class Config:
    organization_id = environ.get("ORGANIZATION_ID", "")
    project_id = environ.get("PROJECT_ID", "")
    enviroment = environ.get("MODE", "")
    private_key = base64.b64decode(environ.get("SSL_KEY", "")).decode("utf-8")
    transfer_account = json.loads(environ.get("TRANSFER_ACCOUNT", {}))
    google_credentials = json.loads(environ.get("GOOGLE_CREDENTIALS", {}))
