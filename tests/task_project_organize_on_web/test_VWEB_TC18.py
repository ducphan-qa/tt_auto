import pytest

from pages.helper.project_web_helpers import (
    open_project_web,
    verify_smart_project_selectable,
)

"""test_VWEB_TC18 - Verify Completed smart project is visible and selectable."""


@pytest.mark.regression
@pytest.mark.tc_id("test_VWEB_TC18")
@pytest.mark.tc_title("Verify Completed smart project is visible and selectable.")
def test_verify_completed_smart_project_selectable(authenticated_page):
    open_project_web(authenticated_page)
    verify_smart_project_selectable(authenticated_page, "Completed")
