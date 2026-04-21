from pathlib import Path
from dotenv import load_dotenv

# Load root .env explicitly
env_path = Path.home() / "openclaw" / ".env"
load_dotenv(env_path)

from .run_pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline()
