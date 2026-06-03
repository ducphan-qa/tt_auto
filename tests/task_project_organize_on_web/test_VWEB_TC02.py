import pytest

from pages.helper.project_web_helpers import open_project_web
from pages.web.side_bar import SideBar

"""test_VWEB_TC02 - Verify smart projects are visible."""


@pytest.mark.regression
@pytest.mark.tc_id("test_VWEB_TC02")
@pytest.mark.tc_title("Verify smart projects are visible.")
def test_verify_smart_projects_are_visible(authenticated_page):
    open_project_web(authenticated_page)
    SideBar(authenticated_page).verify_smart_projects_visible()
