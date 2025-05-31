import os
from dotenv import load_dotenv

load_dotenv()

GLOBAL_CONFIG = {
    "agent": {
        "key": os.getenv("OPENAI_API_KEY"),
        "model": "gpt-4o"
        # "key": os.getenv("CLAUDE_KEY"),
        # "model": "claude-3-5-sonnet-20241022"
    },
    "logger": {
        "level": 1,
    },
    "long_term_memory": {
        "trial": {
            "min": 0,
            "max": 30
        },
        "rule": {
            "min": 0,
            "max": 30
        }
    },
    "session": {
        "training": {
            "window_size": 5
        },
    },
    "simulator": {
        "headless": False,
        "user_data_dir": os.getenv("CHROME_USER_DATA_DIR"),
        "binary_location": os.getenv("CHROME_TESTING_PATH")
    },
}
