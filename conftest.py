import base64
import logging
import os
from datetime import datetime
from typing import Generator

import dotenv
import pytest
from playwright.sync_api import APIRequestContext, Browser, Page, Playwright

from pages.web import config

try:
    from pytest_html import extras as pytest_html_extras
except ImportError:
    pytest_html_extras = None

dotenv.load_dotenv()
TICKTICK_API_URL = os.getenv("TICKTICK_API_URL")
API_KEY = os.getenv("API_KEY")

assert TICKTICK_API_URL, "TICKTICK_API_URL is not set"
assert API_KEY, "API_KEY is not set"


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    request_context = playwright.request.new_context(
        base_url=TICKTICK_API_URL, extra_http_headers=headers
    )
    logging.info("Sending API request")
    yield request_context
    request_context.dispose()


@pytest.fixture()
def authenticated_page(browser: Browser) -> Generator[Page, None, None]:
    assert config.STATE_FILE.exists(), (
        f"Missing saved login state: {config.STATE_FILE}. "
        "Run `python pages/web/generate_state.py` first."
    )

    context = browser.new_context(storage_state=str(config.STATE_FILE))
    page = context.new_page()

    try:
        yield page
    finally:
        context.close()


@pytest.fixture(autouse=True)
def log_test_case_name(request):
    test_module = request.node.module
    test_case_name = getattr(test_module, "test_case_name", request.node.name)
    logging.debug("Starting test case: %s", test_case_name)

    yield

    logging.debug("Finished test case: %s", test_case_name)


@pytest.fixture(autouse=True)
def fail_test_on_warning_or_error(request):
    failed_logs = []

    class WarningErrorHandler(logging.Handler):
        def emit(self, record):
            if record.levelno >= logging.WARNING:
                failed_logs.append(f"{record.levelname}: {record.getMessage()}")

    handler = WarningErrorHandler()
    handler.setLevel(logging.WARNING)
    request.node.warning_error_logs = failed_logs
    logging.getLogger().addHandler(handler)

    yield

    logging.getLogger().removeHandler(handler)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when != "call":
        return

    failed_logs = getattr(item, "warning_error_logs", [])
    if report.passed and failed_logs:
        messages = "\n".join(failed_logs)
        report.outcome = "failed"
        report.longrepr = (
            "Test failed because WARNING or ERROR logs were found:\n"
            f"{messages}"
        )

    if report.failed:
        _capture_and_attach_failure_screenshot(item, report)


def _capture_and_attach_failure_screenshot(item, report):
    attach_failure_screenshots = os.getenv("ATTACH_FAILURE_SCREENSHOTS", "").lower()
    screenshots_enabled = attach_failure_screenshots in {"1", "true", "yes", "on"}
    if os.getenv("CI", "").lower() == "true" and not screenshots_enabled:
        return

    page = item.funcargs.get("authenticated_page") or item.funcargs.get("page")
    if not page:
        return

    screenshot_dir = "reports/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(
        screenshot_dir,
        f"{item.name}_{timestamp}.png",
    )

    try:
        page.screenshot(path=screenshot_path, full_page=True)
        logging.info("Screenshot saved: %s", screenshot_path)
    except Exception as error:
        logging.error("Cannot capture failure screenshot: %s", error)
        return

    if pytest_html_extras is None:
        return

    try:
        with open(screenshot_path, "rb") as screenshot_file:
            screenshot_base64 = base64.b64encode(screenshot_file.read()).decode(
                "utf-8"
            )

        report.extras = getattr(report, "extras", [])
        report.extras.append(
            pytest_html_extras.png(screenshot_base64, name="Failure Screenshot")
        )
    except Exception as error:
        logging.error("Cannot attach screenshot to pytest-html report: %s", error)

