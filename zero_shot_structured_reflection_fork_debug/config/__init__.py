import os
from dotenv import load_dotenv

load_dotenv()

GLOBAL_CONFIG = {
    "agent": {
        "key": os.getenv("OPENAI_API_KEY"),
        "model": "gpt-4o"
    },
    "simulator": {
        "headless": False,
        "user_data_dir": os.getenv("CHROME_USER_DATA_DIR"),
    },
}
