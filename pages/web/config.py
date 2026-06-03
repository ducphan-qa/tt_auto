import os
from pathlib import Path

TICKTICK_URL_SIGNIN = "https://ticktick.com/signin"
TICKTICK_URL_WEBAPP = "https://ticktick.com/webapp"
STATE_FILE = Path(
    os.getenv("TICKTICK_STATE_PATH", Path(__file__).parent / "state.json")
)
