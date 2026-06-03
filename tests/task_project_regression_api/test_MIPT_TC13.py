import pytest

from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import (
    NEGATIVE_STATUSES,
    assert_task_values,
    create_task,
    delete_task_if_exists,
)

"""test_MIPT_TC13 - Reject move with invalid toProjectId."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.xfail(reason="TickTick Open API v1 currently returns 200 for invalid toProjectId moves.")
@pytest.mark.tc_id("test_MIPT_TC13")
@pytest.mark.tc_title("Reject move with invalid toProjectId.")
def test_reject_move_with_invalid_to_project_id(api_request_context):
    task = TaskOrganize(api_request_context)
    source_project_id = task.project_id_default
    invalid_project_id = "invalid_to_project_id_999999"
    task_id = None

    try:
        created_task, title, content = create_task(task, "REG013", project_id=source_project_id)
        task_id = created_task["id"]

        move_response = task.move_task(
            source_project_id,
            invalid_project_id,
            task_id,
            expected_status=(200, *NEGATIVE_STATUSES),
        )
        assert move_response is not None, "Invalid-to move response is empty"
        assert move_response.status != 200

        source_detail = task.get_task(task_id=task_id, project_id=source_project_id)
        assert_task_values(source_detail, task_id, source_project_id, title, content)
    finally:
        delete_task_if_exists(task, task_id, source_project_id)
