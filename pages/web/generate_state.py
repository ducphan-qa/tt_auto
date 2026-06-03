import logging
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pages.web import config
from pages.web.login_page import LoginPage


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    logging.info("Opening browser to generate TickTick login state")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            login_page = LoginPage(page)
            login_page.save_login_session()
        finally:
            browser.close()

    logging.info("TickTick login state saved to %s", config.STATE_FILE)


if __name__ == "__main__":
    main()
