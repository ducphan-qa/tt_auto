import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.project_web_helpers import (
    cleanup_project_web_data,
    create_api_project,
    create_api_task,
    open_project_web,
    verify_project_task_visible,
)
from pages.helper.regression_helpers import unique_text

"""test_GWEB_TC13 - Verify switching projects updates header and visible tasks."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_GWEB_TC13")
@pytest.mark.tc_title("Verify switching from Project A to Project B updates visible tasks.")
def test_verify_switching_projects_updates_visible_tasks(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []
    project_a = unique_text("PROJ WEB Switch A")
    project_b = unique_text("PROJ WEB Switch B")
    task_a = unique_text("PROJ WEB Task A")
    task_b = unique_text("PROJ WEB Task B")

    try:
        project_a_id = create_api_project(project_api, project_a)
        project_b_id = create_api_project(project_api, project_b)
        project_ids.extend([project_a_id, project_b_id])
        task_a_id = create_api_task(task_api, project_a_id, task_a, "Task A")
        task_b_id = create_api_task(task_api, project_b_id, task_b, "Task B")
        task_records.extend([(task_a_id, project_a_id), (task_b_id, project_b_id)])

        open_project_web(authenticated_page)
        verify_project_task_visible(authenticated_page, project_a, task_a)
        verify_project_task_visible(authenticated_page, project_b, task_b)
    finally:
        cleanup_project_web_data(task_api, project_api, task_records, project_ids)
