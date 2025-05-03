import os

def load_env_vars(key):
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Environment variable {key} is missing!")
    return value