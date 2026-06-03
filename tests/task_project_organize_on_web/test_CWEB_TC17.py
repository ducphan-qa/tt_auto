import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.project_web_helpers import (
    cleanup_project_web_data,
    create_api_project,
    create_api_task,
    open_project_web,
    verify_project_row_still_visible_after_tasks,
)
from pages.helper.regression_helpers import unique_text

"""test_CWEB_TC17 - Verify project row remains visible after adding tasks."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_CWEB_TC17")
@pytest.mark.tc_title("Verify API-created project row remains visible after adding tasks.")
def test_verify_project_row_remains_visible_after_adding_tasks(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []
    project_name = unique_text("PROJ WEB Row Count")
    task_titles = [unique_text(f"PROJ WEB Count Task {index}") for index in range(1, 3)]

    try:
        project_id = create_api_project(project_api, project_name)
        project_ids.append(project_id)
        for task_title in task_titles:
            task_id = create_api_task(task_api, project_id, task_title, "Count task")
            task_records.append((task_id, project_id))

        open_project_web(authenticated_page)
        verify_project_row_still_visible_after_tasks(
            authenticated_page,
            project_name,
            task_titles,
        )
    finally:
        cleanup_project_web_data(task_api, project_api, task_records, project_ids)
