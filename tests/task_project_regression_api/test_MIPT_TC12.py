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

"""test_MIPT_TC12 - Reject move with invalid fromProjectId."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.xfail(reason="TickTick Open API v1 currently returns 200 for invalid fromProjectId moves.")
@pytest.mark.tc_id("test_MIPT_TC12")
@pytest.mark.tc_title("Reject move with invalid fromProjectId.")
def test_reject_move_with_invalid_from_project_id(api_request_context):
    project = ProjectOrganize(api_request_context)
    task = TaskOrganize(api_request_context)
    source_project_id = task.project_id_default
    target_project_id = None
    task_id = None
    invalid_project_id = "invalid_from_project_id_999999"

    try:
        target_project_id = create_temp_project(project, "REG012 Target Project")
        created_task, title, content = create_task(task, "REG012", project_id=source_project_id)
        task_id = created_task["id"]

        move_response = task.move_task(
            invalid_project_id,
            target_project_id,
            task_id,
            expected_status=(200, *NEGATIVE_STATUSES),
        )
        assert move_response is not None, "Invalid-from move response is empty"
        assert move_response.status != 200

        source_detail = task.get_task(task_id=task_id, project_id=source_project_id)
        assert_task_values(source_detail, task_id, source_project_id, title, content)
        target_detail = task.get_task(
            task_id=task_id,
            project_id=target_project_id,
            expected_status=404,
        )
        assert target_detail is None
    finally:
        delete_task_if_exists(task, task_id, source_project_id)
        delete_project_if_exists(project, target_project_id)
