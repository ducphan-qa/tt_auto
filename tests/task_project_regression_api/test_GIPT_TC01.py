import pytest

from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import (
    assert_task_values,
    create_task,
    delete_task_if_exists,
)

"""test_GIPT_TC01 - Get task by valid projectId/taskId."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_GIPT_TC01")
@pytest.mark.tc_title("Get task by valid projectId/taskId.")
def test_get_task_by_valid_project_id_and_task_id(api_request_context):
    task = TaskOrganize(api_request_context)
    project_id = task.project_id_default
    task_id = None

    try:
        created_task, title, content = create_task(task, "REG001")
        task_id = created_task["id"]

        task_detail = task.get_task(task_id=task_id, project_id=project_id)

        assert_task_values(task_detail, task_id, project_id, title, content)
        assert task_detail.get("status", 0) == 0
    finally:
        delete_task_if_exists(task, task_id, project_id)
