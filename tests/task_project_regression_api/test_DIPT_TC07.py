import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import create_task, project_task_ids

"""test_DIPT_TC07 - Delete task removes it from project endpoint."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_DIPT_TC07")
@pytest.mark.tc_title("Delete task removes it from project endpoint.")
def test_delete_task_removes_it_from_project_endpoint(api_request_context):
    project = ProjectOrganize(api_request_context)
    task = TaskOrganize(api_request_context)
    project_id = task.project_id_default
    task_id = None

    created_task, _, _ = create_task(task, "REG007", project_id=project_id)
    task_id = created_task["id"]

    delete_response = task.delete_task(task_id=task_id, project_id=project_id)
    assert delete_response is not None, "Delete response is empty"
    assert delete_response.status == 200

    deleted_detail = task.get_task(
        task_id=task_id, project_id=project_id, expected_status=404
    )
    if deleted_detail is not None:
        assert deleted_detail["id"] == task_id

    project_data = project.get_project_with_data(project_id)
    assert task_id not in project_task_ids(project_data)
