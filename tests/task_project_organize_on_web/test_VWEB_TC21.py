import pytest
"""test_VWEB_TC21 - Verify all sidebar elements are visible"""

from pages.web import config
from pages.web.login_page import LoginPage
from pages.web.side_bar import SideBar


@pytest.mark.tc_id("test_VWEB_TC21")
@pytest.mark.tc_title("Verify all sidebar elements are visible")
def test_verify_sidebar_elements(authenticated_page):
    authenticated_page.goto(config.TICKTICK_URL_WEBAPP)
    LoginPage(authenticated_page).assert_app_loaded()

    SideBar(authenticated_page).verify_all_sidebar_elements()
