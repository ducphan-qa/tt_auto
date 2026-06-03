import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.api_web_helpers import (
    cleanup_generated_data,
    create_api_project,
    create_api_task,
    open_web_view,
)
from pages.helper.regression_helpers import unique_text

"""test_CAPIWEB_TC07 - Verify multiple API-generated tasks appear in one project."""


@pytest.mark.api
@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.tc_id("test_CAPIWEB_TC07")
@pytest.mark.tc_title("Verify multiple API-generated tasks appear in one project.")
def test_verify_multiple_api_generated_tasks_on_web(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []

    project_name = unique_text("API WEB Multiple Tasks Project")
    task_titles = [
        unique_text(f"API WEB Multiple Task {index}") for index in range(1, 4)
    ]

    try:
        project_id = create_api_project(project_api, project_name)
        project_ids.append(project_id)
        for task_title in task_titles:
            task_id = create_api_task(
                task_api,
                project_id,
                task_title,
                unique_text("API WEB Multiple Content"),
            )
            task_records.append((task_id, project_id))

        open_web_view(authenticated_page).verify_project_tasks_visible(
            project_name, task_titles
        )
    finally:
        cleanup_generated_data(task_api, project_api, task_records, project_ids)
