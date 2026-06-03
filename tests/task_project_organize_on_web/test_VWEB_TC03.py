import pytest

from pages.helper.project_web_helpers import open_project_web
from pages.web.side_bar import SideBar

"""test_VWEB_TC03 - Verify sidebar project sections are visible."""


@pytest.mark.regression
@pytest.mark.tc_id("test_VWEB_TC03")
@pytest.mark.tc_title("Verify Lists, Filters, and Tags sections are visible.")
def test_verify_sidebar_project_sections_are_visible(authenticated_page):
    open_project_web(authenticated_page)
    SideBar(authenticated_page).verify_sidebar_sections_visible()
