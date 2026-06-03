import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import create_task, delete_task_if_exists

"""test_GIPT_TC17 - Project undone list includes active child tasks."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_GIPT_TC17")
@pytest.mark.tc_title("Project undone list includes active child tasks.")
def test_project_undone_list_includes_active_child_tasks(api_request_context):
    project = ProjectOrganize(api_request_context)
    task = TaskOrganize(api_request_context)
    project_id = task.project_id_default
    parent_task_id = None
    child_task_id = None

    try:
        parent_task, _, _ = create_task(task, "REG017 Parent", project_id=project_id)
        parent_task_id = parent_task["id"]
        child_task, _, _ = create_task(
            task,
            "REG017 Child",
            project_id=project_id,
            extra_fields={"parentId": parent_task_id},
        )
        child_task_id = child_task["id"]

        project_data = project.get_project_with_data(project_id)
        tasks_by_id = {item.get("id"): item for item in project_data.get("tasks", [])}

        assert parent_task_id in tasks_by_id
        assert child_task_id in tasks_by_id
        assert tasks_by_id[child_task_id].get("projectId") == project_id
        assert tasks_by_id[child_task_id].get("parentId") == parent_task_id
    finally:
        delete_task_if_exists(task, child_task_id, project_id)
        delete_task_if_exists(task, parent_task_id, project_id)
