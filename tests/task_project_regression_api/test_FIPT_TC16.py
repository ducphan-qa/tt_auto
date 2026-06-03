import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import (
    create_task,
    create_temp_project,
    delete_project_if_exists,
    delete_task_if_exists,
)

"""test_FIPT_TC16 - Filter workflow returns only project tasks."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_FIPT_TC16")
@pytest.mark.tc_title("Filter workflow returns only project tasks.")
def test_filter_workflow_returns_only_project_tasks(api_request_context):
    project = ProjectOrganize(api_request_context)
    task = TaskOrganize(api_request_context)
    source_project_id = task.project_id_default
    other_project_id = None
    source_task_id = None
    other_task_id = None

    try:
        other_project_id = create_temp_project(project, "REG016 Other Project")
        source_task, _, _ = create_task(task, "REG016 Source", project_id=source_project_id)
        other_task, _, _ = create_task(task, "REG016 Other", project_id=other_project_id)
        source_task_id = source_task["id"]
        other_task_id = other_task["id"]

        filtered_tasks = task.filter_tasks_by_project(project_id=source_project_id, status=0)
        filtered_ids = [item.get("id") for item in filtered_tasks]

        assert source_task_id in filtered_ids
        assert other_task_id not in filtered_ids
        assert all(item.get("projectId") == source_project_id for item in filtered_tasks)
    finally:
        delete_task_if_exists(task, source_task_id, source_project_id)
        delete_task_if_exists(task, other_task_id, other_project_id)
        delete_project_if_exists(project, other_project_id)
