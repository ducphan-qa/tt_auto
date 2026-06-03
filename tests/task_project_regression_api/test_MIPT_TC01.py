from datetime import datetime

import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize

"""test_MIPT_TC01 - Move task from Project A to Project B successfully"""

current_task_title = "TP01 - Move task from Project A to Project B"
current_task_content = "Task content should remain unchanged after move."


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_MIPT_TC01")
@pytest.mark.tc_title("Move task from Project A to Project B successfully")
def test_move_task_from_project_A_to_project_B(api_request_context):
    project = ProjectOrganize(api_request_context)
    task = TaskOrganize(api_request_context)

    from_project_id = task.project_id_default
    to_project_id = None
    task_id = None
    task_moved = False

    try:
        project_name = (
            "TP01 - Move Task Destination " f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        project_body = {
            "name": project_name,
            "viewMode": "list",
            "kind": "TASK",
        }

        created_project = project.create_project(project_body)
        assert created_project is not None, "Create destination project failed"
        assert (
            "id" in created_project
        ), f"Destination project id not found. Response: {created_project}"
        to_project_id = created_project["id"]

        created_task = task.create_task(
            task_title=current_task_title,
            task_content=current_task_content,
        )
        assert created_task is not None, "Create task in source project failed"
        assert "id" in created_task, f"Task id not found. Response: {created_task}"
        task_id = created_task["id"]

        move_response = task.move_task(from_project_id, to_project_id, task_id)
        assert move_response is not None, "Move task response is empty"
        assert (
            move_response.status == 200
        ), f"Expected move status 200 but got {move_response.status}"
        task_moved = True

        task.project_id_default = to_project_id
        moved_task_detail = task.get_task(task_id=task_id)
        assert moved_task_detail is not None, "Task not found in destination project"
        assert moved_task_detail["id"] == task_id
        assert moved_task_detail["projectId"] == to_project_id
        assert moved_task_detail["title"] == current_task_title
        assert moved_task_detail["content"] == current_task_content

        task.project_id_default = from_project_id
        source_task_detail = task.get_task(task_id=task_id, expected_status=404)
        assert source_task_detail is None, "Task still belongs to source project"

    finally:
        if task_id:
            task.project_id_default = to_project_id if task_moved else from_project_id
            task.delete_task(task_id=task_id)

        if to_project_id:
            project.delele_project(to_project_id)
