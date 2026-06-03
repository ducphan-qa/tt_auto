import pytest

from pages.api.task_organize import TaskOrganize

"""test_MIPT_TC04 - Move task to invalid destination project"""

current_task_title = "TP04 - Move task to invalid destination project"
current_task_content = "Task should remain in source project after failed move."
invalid_project_id = "invalid_project_id_999999"
accepted_move_statuses = (200, 400, 404)


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_MIPT_TC04")
@pytest.mark.tc_title("Move task to invalid destination project")
def test_move_task_to_invalid_destination_project(api_request_context):
    task = TaskOrganize(api_request_context)

    from_project_id = task.project_id_default
    task_id = None

    try:
        created_task = task.create_task(
            task_title=current_task_title,
            task_content=current_task_content,
        )
        assert created_task is not None, "Create task in source project failed"
        assert "id" in created_task, f"Task id not found. Response: {created_task}"
        task_id = created_task["id"]

        move_response = task.move_task(
            from_project_id,
            invalid_project_id,
            task_id,
            expected_status=accepted_move_statuses,
        )
        assert move_response is not None, "Move task response is empty"
        assert move_response.status in accepted_move_statuses, (
            "Expected move status 200, 400, or 404 but got "
            f"{move_response.status}"
        )

        task.project_id_default = from_project_id
        source_task_detail = task.get_task(task_id=task_id)
        assert source_task_detail is not None, "Task not found in source project"
        assert source_task_detail["id"] == task_id
        assert source_task_detail["projectId"] == from_project_id
        assert source_task_detail["title"] == current_task_title
        assert source_task_detail["content"] == current_task_content

    finally:
        if task_id:
            task.project_id_default = from_project_id
            task.delete_task(task_id=task_id)
