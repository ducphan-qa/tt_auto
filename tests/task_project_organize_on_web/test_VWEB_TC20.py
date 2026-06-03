import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.project_web_helpers import (
    cleanup_project_web_data,
    create_api_project,
    open_project_web,
    verify_project_navigation_keeps_shell_visible,
)
from pages.helper.regression_helpers import unique_text

"""test_VWEB_TC20 - Verify project navigation keeps sidebar and quick-add visible."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_VWEB_TC20")
@pytest.mark.tc_title("Verify project navigation does not hide sidebar sections or quick-add.")
def test_verify_project_navigation_keeps_sidebar_and_quick_add_visible(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []
    project_name = unique_text("PROJ WEB Shell")

    try:
        project_id = create_api_project(project_api, project_name)
        project_ids.append(project_id)
        open_project_web(authenticated_page)
        verify_project_navigation_keeps_shell_visible(authenticated_page, project_name)
    finally:
        cleanup_project_web_data(task_api, project_api, task_records, project_ids)
