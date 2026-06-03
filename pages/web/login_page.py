import os
import logging

import dotenv
from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

from pages.web import config

dotenv.load_dotenv()


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.base_url = config.TICKTICK_URL_SIGNIN
        self.__user = (
            os.getenv("TICKTICK_USERNAME")
            or os.getenv("TICKTICK_USER")
            or os.getenv("USER")
        )
        self.__pass = (
            os.getenv("TICKTICK_PASSWORD")
            or os.getenv("TICKTICK_PASS")
            or os.getenv("PASS")
        )

        assert self.base_url, "TICKTICK_URL_SIGNIN is not set"

    def _open_sign_in_if_needed(self) -> None:
        if "/signin" in self.page.url or "/login" in self.page.url:
            return

        try:
            self.page.wait_for_selector("input[type='password']", timeout=3000)
            return
        except PlaywrightTimeoutError:
            logging.info("TickTick sign-in form is not visible yet; opening it")

        self._click_first_visible(
            [
                "a[href*='signin']",
                "a[href*='login']",
                "button:has-text('Sign In')",
                "button:has-text('Log In')",
                "text=/^(Sign In|Log In|Login)$/i",
            ],
            "TickTick sign-in entry point",
        )
        self.page.wait_for_selector("input[type='password']", timeout=15000)

    def assert_app_loaded(self) -> None:
        self.page.wait_for_load_state("networkidle")

        success_selectors = [
            "[data-testid*='task' i]",
            "[class*='task' i]",
            "[class*='project' i]",
            "[aria-label*='task' i]",
            "text=/Inbox|Today|Next 7 Days|Task/i",
        ]

        for selector in success_selectors:
            try:
                self.page.locator(selector).first.wait_for(
                    state="visible",
                    timeout=5000,
                )
                return
            except PlaywrightTimeoutError:
                continue

        raise AssertionError(
            "TickTick login did not reach the main app/task UI after submitting"
        )

    def verify_saved_login_session(self) -> None:
        self.page.goto(config.TICKTICK_URL_WEBAPP)
        self.assert_app_loaded()

    def _fill_first_visible(self, selectors: list[str], value: str, name: str) -> None:
        for selector in selectors:
            locator = self.page.locator(selector).first
            try:
                locator.wait_for(state="visible", timeout=5000)
                locator.fill(value)
                return
            except PlaywrightTimeoutError:
                continue

        raise AssertionError(f"Cannot find {name}")

    def _click_first_visible(self, selectors: list[str], name: str) -> None:
        for selector in selectors:
            locator = self.page.locator(selector).first
            try:
                locator.wait_for(state="visible", timeout=5000)
                locator.click()
                return
            except PlaywrightTimeoutError:
                continue

        raise AssertionError(f"Cannot find {name}")

    def login_to_ticktick(self) -> None:
        assert self.__user, "TICKTICK_USERNAME is not set"
        assert self.__pass, "TICKTICK_PASSWORD is not set"

        self.page.goto(self.base_url)
        self._open_sign_in_if_needed()
        self._fill_first_visible(
            [
                "input[name='username']",
                "input[name='email']",
                "input[type='email']",
                "input[autocomplete='username']",
                "input[placeholder*='Email' i]",
                "input[placeholder*='Username' i]",
                "input[placeholder*='Phone' i]",
            ],
            self.__user,
            "TickTick username/email field",
        )
        self._fill_first_visible(
            [
                "input[name='password']",
                "input[type='password']",
                "input[autocomplete='current-password']",
                "input[placeholder*='Password' i]",
            ],
            self.__pass,
            "TickTick password field",
        )
        self._click_first_visible(
            [
                "button[type='submit']",
                "button:has-text('Sign In')",
                "button:has-text('Log In')",
                "button:has-text('Login')",
            ],
            "TickTick sign-in button",
        )
        self.assert_app_loaded()

    def save_login_session(self) -> None:
        self.login_to_ticktick()
        config.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.page.context.storage_state(path=str(config.STATE_FILE))
        logging.info("Session saved to %s", config.STATE_FILE)
