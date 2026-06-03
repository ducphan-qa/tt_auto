import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import (
    NEGATIVE_STATUSES,
    assert_negative_task_response,
    assert_task_values,
    create_task,
    create_temp_project,
    delete_project_if_exists,
    delete_task_if_exists,
)

"""test_GIPT_TC02 - Reject get task with wrong projectId."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_GIPT_TC02")
@pytest.mark.tc_title("Reject get task with wrong projectId.")
def test_reject_get_task_with_wrong_project_id(api_request_context):
    project = ProjectOrganize(api_request_context)
    task = TaskOrganize(api_request_context)
    source_project_id = task.project_id_default
    wrong_project_id = None
    task_id = None

    try:
        wrong_project_id = create_temp_project(project, "REG002 Wrong Project")
        created_task, title, content = create_task(task, "REG002", project_id=source_project_id)
        task_id = created_task["id"]

        wrong_response = task.get_task(
            task_id=task_id,
            project_id=wrong_project_id,
            expected_status=NEGATIVE_STATUSES,
        )
        assert_negative_task_response(
            wrong_response,
            "Wrong-project get should be rejected or return not found",
        )

        source_detail = task.get_task(task_id=task_id, project_id=source_project_id)
        assert_task_values(source_detail, task_id, source_project_id, title, content)
    finally:
        delete_task_if_exists(task, task_id, source_project_id)
        delete_project_if_exists(project, wrong_project_id)
