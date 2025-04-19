import os
from termcolor import cprint

def get_env_var(key: str, default=None):
    value = os.getenv(key, default)
    if value is None:
        cprint(f"[WARN] Environment variable '{key}' not set.", "red")
    return value
