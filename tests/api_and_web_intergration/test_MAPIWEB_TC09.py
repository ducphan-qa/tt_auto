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

"""test_MAPIWEB_TC09 - Verify API-moved task appears in destination project on web."""


@pytest.mark.api
@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.tc_id("test_MAPIWEB_TC09")
@pytest.mark.tc_title("Verify API-moved task appears in destination project on web.")
def test_verify_api_moved_task_contents_on_web(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []

    source_project_name = unique_text("API WEB Move Source Project")
    destination_project_name = unique_text("API WEB Move Destination Project")
    task_title = unique_text("API WEB Moved Task")
    task_content = unique_text("API WEB Moved Content")

    try:
        source_project_id = create_api_project(project_api, source_project_name)
        destination_project_id = create_api_project(
            project_api, destination_project_name
        )
        project_ids.extend([source_project_id, destination_project_id])

        task_id = create_api_task(task_api, source_project_id, task_title, task_content)
        task_records.append((task_id, source_project_id))

        move_response = task_api.move_task(
            source_project_id, destination_project_id, task_id
        )
        assert move_response is not None, "Move task response is empty"
        assert move_response.status == 200
        task_records[-1] = (task_id, destination_project_id)

        open_web_view(authenticated_page).verify_project_task_contents(
            destination_project_name, task_title, task_content
        )
    finally:
        cleanup_generated_data(task_api, project_api, task_records, project_ids)
