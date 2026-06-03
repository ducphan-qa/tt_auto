import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.project_web_helpers import (
    cleanup_project_web_data,
    create_api_project,
    create_api_task,
    open_project_web,
    verify_project_tasks_visible,
)
from pages.helper.regression_helpers import unique_text

"""test_CWEB_TC07 - Verify project with multiple tasks shows all task rows."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_CWEB_TC07")
@pytest.mark.tc_title("Verify API-created project with multiple tasks shows all task rows.")
def test_verify_project_with_multiple_tasks_shows_all_rows(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []
    project_name = unique_text("PROJ WEB Multi Task")
    task_titles = [unique_text(f"PROJ WEB Task {index}") for index in range(1, 4)]

    try:
        project_id = create_api_project(project_api, project_name)
        project_ids.append(project_id)
        for task_title in task_titles:
            task_id = create_api_task(task_api, project_id, task_title, "Multi task")
            task_records.append((task_id, project_id))

        open_project_web(authenticated_page)
        verify_project_tasks_visible(authenticated_page, project_name, task_titles)
    finally:
        cleanup_project_web_data(task_api, project_api, task_records, project_ids)
