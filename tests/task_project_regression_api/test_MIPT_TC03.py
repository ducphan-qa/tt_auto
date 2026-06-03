from datetime import datetime

import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize

"""test_MIPT_TC03 - Move non-existing task"""

invalid_task_id = "invalid_task_id_999999"
accepted_move_statuses = (200, 400, 404)


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_MIPT_TC03")
@pytest.mark.tc_title("Move non-existing task")
def test_move_non_existing_task(api_request_context):
    project = ProjectOrganize(api_request_context)
    task = TaskOrganize(api_request_context)

    from_project_id = task.project_id_default
    to_project_id = None

    try:
        project_name = (
            "TP03 - Move Task Destination "
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        project_body = {
            "name": project_name,
            "viewMode": "list",
            "kind": "TASK",
        }

        created_project = project.create_project(project_body)
        assert created_project is not None, "Create destination project failed"
        assert "id" in created_project, (
            f"Destination project id not found. Response: {created_project}"
        )
        to_project_id = created_project["id"]

        move_response = task.move_task(
            from_project_id,
            to_project_id,
            invalid_task_id,
            expected_status=accepted_move_statuses,
        )
        assert move_response is not None, "Move invalid task response is empty"
        assert move_response.status in accepted_move_statuses, (
            "Expected move status 200, 400, or 404 but got "
            f"{move_response.status}"
        )

        destination_project_data = project.get_project_with_data(to_project_id)
        assert destination_project_data is not None, (
            "Destination project data response is empty"
        )
        destination_tasks = destination_project_data.get("tasks", [])
        destination_task_ids = [item.get("id") for item in destination_tasks]
        assert invalid_task_id not in destination_task_ids, (
            "Invalid task unexpectedly exists in destination project data"
        )

    finally:
        if to_project_id:
            project.delele_project(to_project_id)
