import pytest

from pages.helper.project_web_helpers import (
    open_project_web,
    verify_smart_project_selectable,
)

"""test_VWEB_TC19 - Verify Trash smart project is visible and selectable."""


@pytest.mark.regression
@pytest.mark.tc_id("test_VWEB_TC19")
@pytest.mark.tc_title("Verify Trash smart project is visible and selectable.")
def test_verify_trash_smart_project_selectable(authenticated_page):
    open_project_web(authenticated_page)
    verify_smart_project_selectable(authenticated_page, "Trash")
