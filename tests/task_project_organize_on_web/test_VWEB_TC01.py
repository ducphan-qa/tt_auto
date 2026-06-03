import pytest

from pages.helper.project_web_helpers import open_project_web, verify_project_list_visible

"""test_VWEB_TC01 - Verify project list sidebar root and scroller are visible."""


@pytest.mark.regression
@pytest.mark.tc_id("test_VWEB_TC01")
@pytest.mark.tc_title("Verify project list sidebar root and scroller are visible.")
def test_verify_project_list_sidebar_root_and_scroller(authenticated_page):
    open_project_web(authenticated_page)
    verify_project_list_visible(authenticated_page)
