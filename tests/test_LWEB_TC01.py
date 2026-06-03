import pytest
"""test_LWEB_TC01 - Verify saved login session successfully"""

from pages.web.login_page import LoginPage


@pytest.mark.tc_id("test_LWEB_TC01")
@pytest.mark.tc_title("Verify saved login session successfully")
def test_login(authenticated_page):
    LoginPage(authenticated_page).verify_saved_login_session()
