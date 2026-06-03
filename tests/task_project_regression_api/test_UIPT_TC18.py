import pytest

from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import create_task, delete_task_if_exists

"""test_UIPT_TC18 - Completing parent does not corrupt child project linkage."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_UIPT_TC18")
@pytest.mark.tc_title("Completing parent does not corrupt child project linkage.")
def test_completing_parent_does_not_corrupt_child_project_linkage(api_request_context):
    task = TaskOrganize(api_request_context)
    project_id = task.project_id_default
    parent_task_id = None
    child_task_id = None

    try:
        parent_task, _, _ = create_task(task, "REG018 Parent", project_id=project_id)
        parent_task_id = parent_task["id"]
        child_task, _, _ = create_task(
            task,
            "REG018 Child",
            project_id=project_id,
            extra_fields={"parentId": parent_task_id},
        )
        child_task_id = child_task["id"]

        complete_response = task.complete_task(project_id, parent_task_id)
        assert complete_response is not None, "Complete parent response is empty"
        assert complete_response.status == 200

        child_detail = task.get_task(task_id=child_task_id, project_id=project_id)
        assert child_detail["id"] == child_task_id
        assert child_detail["projectId"] == project_id
        assert child_detail.get("parentId") == parent_task_id
    finally:
        delete_task_if_exists(task, child_task_id, project_id)
        delete_task_if_exists(task, parent_task_id, project_id)
