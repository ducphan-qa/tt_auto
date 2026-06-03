import pytest

from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import (
    assert_task_values,
    create_task,
    delete_task_if_exists,
)

"""test_CIPT_TC03 - Create task assigns requested projectId."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_CIPT_TC03")
@pytest.mark.tc_title("Create task assigns requested projectId.")
def test_create_task_assigns_requested_project_id(api_request_context):
    task = TaskOrganize(api_request_context)
    project_id = task.project_id_default
    task_id = None

    try:
        created_task, title, content = create_task(
            task, "REG003", project_id=project_id
        )
        task_id = created_task["id"]

        assert created_task["projectId"] == project_id
        task_detail = task.get_task(task_id=task_id, project_id=project_id)
        assert_task_values(task_detail, task_id, project_id, title, content)
    finally:
        delete_task_if_exists(task, task_id, project_id)
