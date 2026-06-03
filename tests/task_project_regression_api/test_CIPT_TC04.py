import pytest

from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import (
    NEGATIVE_STATUSES,
    delete_task_if_exists,
    unique_text,
)

"""test_CIPT_TC04 - Reject create task with invalid projectId."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.xfail(
    reason="TickTick Open API v1 currently creates invalid-project tasks in Inbox."
)
@pytest.mark.tc_id("test_CIPT_TC04")
@pytest.mark.tc_title("Reject create task with invalid projectId.")
def test_reject_create_task_with_invalid_project_id(api_request_context):
    task = TaskOrganize(api_request_context)
    invalid_project_id = "invalid_project_id_999999"
    unique_title = unique_text("REG004 Invalid Project")
    created_task_id = None
    created_project_id = None

    try:
        create_response = task.create_task(
            task_title=unique_title,
            task_content="Task should not be created",
            project_id=invalid_project_id,
            expected_status=(200, *NEGATIVE_STATUSES),
        )
        assert create_response is not None, "Create invalid project response is empty"
        if isinstance(create_response, dict):
            created_task_id = create_response.get("id")
            created_project_id = create_response.get("projectId")
            assert created_project_id == invalid_project_id
        else:
            assert create_response.status != 200

        search_results = task.search_tasks_by_title(unique_title)
        assert search_results == []
    finally:
        delete_task_if_exists(task, created_task_id, created_project_id)
