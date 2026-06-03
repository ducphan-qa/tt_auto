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

"""test_CAPIWEB_TC01 - Verify API-generated project and task content on web."""


@pytest.mark.api
@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.tc_id("test_CAPIWEB_TC01")
@pytest.mark.tc_title("Verify API-generated project and task content on web.")
def test_verify_api_generated_project_and_task_contents_on_web(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []

    project_name = unique_text("API WEB Project")
    task_title = unique_text("API WEB Task")
    task_content = unique_text("API WEB Content")

    try:
        project_id = create_api_project(project_api, project_name)
        project_ids.append(project_id)
        task_id = create_api_task(task_api, project_id, task_title, task_content)
        task_records.append((task_id, project_id))

        open_web_view(authenticated_page).verify_project_task_contents(
            project_name, task_title, task_content
        )
    finally:
        cleanup_generated_data(task_api, project_api, task_records, project_ids)
