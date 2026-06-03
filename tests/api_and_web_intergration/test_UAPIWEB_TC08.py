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

"""test_UAPIWEB_TC08 - Verify API-updated task content appears on web."""


@pytest.mark.api
@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.tc_id("test_UAPIWEB_TC08")
@pytest.mark.tc_title("Verify API-updated task content appears on web.")
def test_verify_api_updated_task_contents_on_web(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []

    project_name = unique_text("API WEB Update Project")
    original_title = unique_text("API WEB Original Task")
    original_content = unique_text("API WEB Original Content")
    updated_title = unique_text("API WEB Updated Task")
    updated_content = unique_text("API WEB Updated Content")

    try:
        project_id = create_api_project(project_api, project_name)
        project_ids.append(project_id)
        task_id = create_api_task(task_api, project_id, original_title, original_content)
        task_records.append((task_id, project_id))

        update_response = task_api.update_task(
            task_id,
            {
                "id": task_id,
                "projectId": project_id,
                "title": updated_title,
                "content": updated_content,
                "priority": 1,
            },
        )
        assert update_response is not None, "Update task response is empty"

        open_web_view(authenticated_page).verify_project_task_contents(
            project_name, updated_title, updated_content
        )
    finally:
        cleanup_generated_data(task_api, project_api, task_records, project_ids)
