import pytest

from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import create_task, delete_task_if_exists

"""test_UIPT_TC09 - Complete task requires correct projectId."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_UIPT_TC09")
@pytest.mark.tc_title("Complete task requires correct projectId.")
def test_complete_task_requires_correct_project_id(api_request_context):
    task = TaskOrganize(api_request_context)
    project_id = task.project_id_default
    task_id = None

    try:
        created_task, _, _ = create_task(task, "REG009", project_id=project_id)
        task_id = created_task["id"]

        complete_response = task.complete_task(project_id, task_id)
        assert complete_response is not None, "Complete response is empty"
        assert complete_response.status == 200

        active_tasks = task.filter_tasks_by_project(project_id=project_id, status=0)
        active_task_ids = [item.get("id") for item in active_tasks]
        assert task_id not in active_task_ids
    finally:
        delete_task_if_exists(task, task_id, project_id)
