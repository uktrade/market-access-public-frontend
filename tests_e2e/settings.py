import os

BASE_URL = os.environ.get("E2E_TEST_BASE_URL", "http://localhost:9980/")
WEB_DRIVER_URL = os.environ.get("WEB_DRIVER_URL")
WEB_DRIVER_NAME = os.environ.get("WEB_DRIVER_URL", "chrome")
HEADLESS_MODE = bool(int(os.environ.get("HEADLESS_MODE", 1)))
