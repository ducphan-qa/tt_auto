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

"""test_UAPIWEB_TC10 - Verify API-renamed project appears on web with its task."""


@pytest.mark.api
@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.tc_id("test_UAPIWEB_TC10")
@pytest.mark.tc_title("Verify API-renamed project appears on web with its task.")
def test_verify_api_renamed_project_with_task_on_web(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []

    original_project_name = unique_text("API WEB Original Project")
    renamed_project_name = unique_text("API WEB Renamed Project")
    task_title = unique_text("API WEB Renamed Project Task")
    task_content = unique_text("API WEB Renamed Project Content")

    try:
        project_id = create_api_project(project_api, original_project_name)
        project_ids.append(project_id)
        task_id = create_api_task(task_api, project_id, task_title, task_content)
        task_records.append((task_id, project_id))

        updated_project = project_api.update_project(
            project_id,
            {
                "name": renamed_project_name,
                "viewMode": "list",
                "kind": "TASK",
            },
        )
        assert updated_project is not None, "Update project response is empty"
        assert updated_project["name"] == renamed_project_name

        open_web_view(authenticated_page).verify_project_task_contents(
            renamed_project_name, task_title, task_content
        )
    finally:
        cleanup_generated_data(task_api, project_api, task_records, project_ids)
