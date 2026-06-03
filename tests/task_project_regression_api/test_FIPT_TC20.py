import pytest

from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import (
    assert_task_values,
    create_task,
    delete_task_if_exists,
)

"""test_FIPT_TC20 - Search workflow result can be validated through project endpoint."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_FIPT_TC20")
@pytest.mark.tc_title("Search workflow result can be validated through project endpoint.")
def test_search_workflow_result_can_be_validated_through_project_endpoint(api_request_context):
    task = TaskOrganize(api_request_context)
    project_id = task.project_id_default
    task_id = None

    try:
        created_task, title, content = create_task(task, "REG020 Search", project_id=project_id)
        task_id = created_task["id"]

        search_results = task.search_tasks_by_title(title, project_id=project_id)
        search_ids = [item.get("id") for item in search_results]
        assert task_id in search_ids

        task_detail = task.get_task(task_id=task_id, project_id=project_id)
        assert_task_values(task_detail, task_id, project_id, title, content)
    finally:
        delete_task_if_exists(task, task_id, project_id)
