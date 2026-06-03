import pytest

from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import (
    assert_task_values,
    create_task,
    delete_task_if_exists,
    unique_text,
)

"""test_UIPT_TC05 - Update task content preserves projectId."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_UIPT_TC05")
@pytest.mark.tc_title("Update task content preserves projectId.")
def test_update_task_content_preserves_project_id(api_request_context):
    task = TaskOrganize(api_request_context)
    project_id = task.project_id_default
    task_id = None

    try:
        created_task, _, _ = create_task(task, "REG005", project_id=project_id)
        task_id = created_task["id"]
        updated_title = unique_text("REG005 Updated Title")
        updated_content = unique_text("REG005 Updated Content")

        update_body = {
            "id": task_id,
            "projectId": project_id,
            "title": updated_title,
            "content": updated_content,
            "priority": 1,
        }
        updated_task = task.update_task(task_id, update_body)
        assert updated_task is not None, "Update task response is empty"

        task_detail = task.get_task(task_id=task_id, project_id=project_id)
        assert_task_values(
            task_detail, task_id, project_id, updated_title, updated_content
        )
    finally:
        delete_task_if_exists(task, task_id, project_id)
