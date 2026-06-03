import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import (
    assert_task_values,
    create_task,
    create_temp_project,
    delete_project_if_exists,
    delete_task_if_exists,
    unique_text,
)

"""test_UIPT_TC06 - Update task with mismatched projectId is safe."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_UIPT_TC06")
@pytest.mark.tc_title("Update task with mismatched projectId is safe.")
def test_update_task_with_mismatched_project_id_is_safe(api_request_context):
    project = ProjectOrganize(api_request_context)
    task = TaskOrganize(api_request_context)
    source_project_id = task.project_id_default
    target_project_id = None
    task_id = None

    try:
        target_project_id = create_temp_project(project, "REG006 Target Project")
        created_task, original_title, original_content = create_task(
            task,
            "REG006",
            project_id=source_project_id,
        )
        task_id = created_task["id"]
        updated_title = unique_text("REG006 Updated")
        updated_content = unique_text("REG006 Content")

        update_body = {
            "id": task_id,
            "projectId": target_project_id,
            "title": updated_title,
            "content": updated_content,
        }
        update_response = task.update_task(task_id, update_body)
        assert update_response is not None, "Update response is empty"

        source_detail = task.get_task(
            task_id=task_id,
            project_id=source_project_id,
            expected_status=(200, 404),
        )
        target_detail = task.get_task(
            task_id=task_id,
            project_id=target_project_id,
            expected_status=(200, 404),
        )
        visible_details = [item for item in (source_detail, target_detail) if item]
        assert len(visible_details) == 1, "Task should exist in exactly one project"

        actual_detail = visible_details[0]
        assert actual_detail["id"] == task_id
        assert actual_detail["projectId"] in (source_project_id, target_project_id)
        assert actual_detail["title"] in (original_title, updated_title)
        assert actual_detail.get("content", "") in (original_content, updated_content)
    finally:
        if task_id:
            delete_task_if_exists(task, task_id, source_project_id)
            delete_task_if_exists(task, task_id, target_project_id)
        delete_project_if_exists(project, target_project_id)
