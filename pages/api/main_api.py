from playwright.sync_api import APIRequestContext
import pytest
import os
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext
import pytest
import dotenv
import logging

TICKTICK_URL = "https://api.ticktick.com/api/v2"
API_KEY = os.getenv("API_KEY")

assert TICKTICK_URL, "TICKTICK_URL is not set"
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
        base_url=TICKTICK_URL, extra_http_headers=headers
    )
    logging.info("Sending API request")
    yield request_context
    request_context.dispose()


class MainAPI:
    def clear_trash(self, api_request_context: APIRequestContext):
        response = api_request_context.delete("/trash/cleanUp")
        assert response.status == 200, f"Expected 200 but got {response.status}"
