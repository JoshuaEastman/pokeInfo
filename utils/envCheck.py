import os
from dotenv import load_dotenv

def load_env():
    env_path = ".env"
    # Check if .env file exists and return True
    if os.path.isfile(env_path):
        load_dotenv(env_path)
        print("Loaded through .env File")
        return True

    # Return false if there is no .env file
    return False