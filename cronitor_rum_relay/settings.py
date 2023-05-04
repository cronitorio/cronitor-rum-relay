import os
import secrets


def is_truthy(value):
    return value and value.lower() in ("1", "true", "yes", "y")


DRY_MODE = is_truthy(os.environ.get("DRY_MODE", "0"))

UPSTREAM_HOST = os.environ.get("UPSTREAM_HOST", "https://rum.cronitor.io")

SECRET_SALT = os.environ.get("SECRET_SALT", secrets.token_hex(32))

GEO_IP_CITY_DATABASE = os.environ.get("GEO_IP_CITY_DATABASE", None)
