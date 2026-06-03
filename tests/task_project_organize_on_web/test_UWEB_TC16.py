import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.project_web_helpers import (
    cleanup_project_web_data,
    create_api_project,
    open_project_web,
    update_api_project,
    verify_selected_project,
)
from pages.helper.regression_helpers import unique_text

"""test_UWEB_TC16 - Verify project with updated color remains selectable."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_UWEB_TC16")
@pytest.mark.tc_title("Verify project with updated color still appears and remains selectable.")
def test_verify_project_with_updated_color_remains_selectable(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []
    project_name = unique_text("PROJ WEB Color")

    try:
        project_id = create_api_project(project_api, project_name, color="#F18181")
        project_ids.append(project_id)
        update_api_project(project_api, project_id, project_name, color="#5E97F6")
        open_project_web(authenticated_page)
        verify_selected_project(authenticated_page, project_name)
    finally:
        cleanup_project_web_data(task_api, project_api, task_records, project_ids)
