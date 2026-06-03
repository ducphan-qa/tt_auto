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

"""test_UIPT_TC10 - Reject complete using wrong projectId."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.xfail(
    reason="TickTick Open API v1 currently returns 200 for wrong-project complete."
)
@pytest.mark.tc_id("test_UIPT_TC10")
@pytest.mark.tc_title("Reject complete using wrong projectId.")
def test_reject_complete_using_wrong_project_id(api_request_context):
    project = ProjectOrganize(api_request_context)
    task = TaskOrganize(api_request_context)
    source_project_id = task.project_id_default
    wrong_project_id = None
    task_id = None

    try:
        wrong_project_id = create_temp_project(project, "REG010 Wrong Project")
        created_task, title, content = create_task(
            task, "REG010", project_id=source_project_id
        )
        task_id = created_task["id"]

        complete_response = task.complete_task(
            wrong_project_id,
            task_id,
            expected_status=(200, *NEGATIVE_STATUSES),
        )
        assert complete_response is not None, "Wrong-project complete response is empty"
        assert complete_response.status != 200

        source_detail = task.get_task(task_id=task_id, project_id=source_project_id)
        assert_task_values(source_detail, task_id, source_project_id, title, content)
        assert source_detail.get("status", 0) == 0
    finally:
        delete_task_if_exists(task, task_id, source_project_id)
        delete_project_if_exists(project, wrong_project_id)
