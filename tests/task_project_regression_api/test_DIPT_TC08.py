import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import (
    NEGATIVE_STATUSES,
    assert_task_values,
    create_task,
    create_temp_project,
    delete_project_if_exists,
    delete_task_if_exists,
)

"""test_DIPT_TC08 - Reject delete using wrong projectId."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.xfail(
    reason="TickTick Open API v1 currently returns 200 for wrong-project delete."
)
@pytest.mark.tc_id("test_DIPT_TC08")
@pytest.mark.tc_title("Reject delete using wrong projectId.")
def test_reject_delete_using_wrong_project_id(api_request_context):
    project = ProjectOrganize(api_request_context)
    task = TaskOrganize(api_request_context)
    source_project_id = task.project_id_default
    wrong_project_id = None
    task_id = None

    try:
        wrong_project_id = create_temp_project(project, "REG008 Wrong Project")
        created_task, title, content = create_task(
            task, "REG008", project_id=source_project_id
        )
        task_id = created_task["id"]

        delete_response = task.delete_task(
            task_id=task_id,
            project_id=wrong_project_id,
            expected_status=(200, *NEGATIVE_STATUSES),
        )
        assert delete_response is not None, "Wrong-project delete response is empty"
        assert delete_response.status != 200

        source_detail = task.get_task(task_id=task_id, project_id=source_project_id)
        assert_task_values(source_detail, task_id, source_project_id, title, content)
    finally:
        delete_task_if_exists(task, task_id, source_project_id)
        delete_project_if_exists(project, wrong_project_id)
