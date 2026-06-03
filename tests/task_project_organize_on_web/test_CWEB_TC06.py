import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.project_web_helpers import (
    cleanup_project_web_data,
    create_api_project,
    create_api_task,
    open_project_web,
    verify_project_task_visible,
)
from pages.helper.regression_helpers import unique_text

"""test_CWEB_TC06 - Verify project with normal task shows task row on web."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_CWEB_TC06")
@pytest.mark.tc_title("Verify API-created project with normal task shows task row on web.")
def test_verify_project_with_normal_task_shows_task_row(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []
    project_name = unique_text("PROJ WEB Normal Task")
    task_title = unique_text("PROJ WEB Task")

    try:
        project_id = create_api_project(project_api, project_name)
        project_ids.append(project_id)
        task_id = create_api_task(task_api, project_id, task_title, "Normal task")
        task_records.append((task_id, project_id))
        open_project_web(authenticated_page)
        verify_project_task_visible(authenticated_page, project_name, task_title)
    finally:
        cleanup_project_web_data(task_api, project_api, task_records, project_ids)
