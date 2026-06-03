import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.project_web_helpers import (
    cleanup_project_web_data,
    create_api_project,
    create_api_task,
    open_project_web,
    verify_task_not_visible,
)
from pages.helper.regression_helpers import unique_text

"""test_GWEB_TC14 - Verify task from Project A is hidden in Project B."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_GWEB_TC14")
@pytest.mark.tc_title("Verify task from Project A is not visible after switching to Project B.")
def test_verify_project_a_task_hidden_after_switch_to_project_b(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []
    project_a = unique_text("PROJ WEB Hidden A")
    project_b = unique_text("PROJ WEB Hidden B")
    task_a = unique_text("PROJ WEB Hidden Task A")

    try:
        project_a_id = create_api_project(project_api, project_a)
        project_b_id = create_api_project(project_api, project_b)
        project_ids.extend([project_a_id, project_b_id])
        task_a_id = create_api_task(task_api, project_a_id, task_a, "Task A")
        task_records.append((task_a_id, project_a_id))

        open_project_web(authenticated_page)
        verify_task_not_visible(authenticated_page, project_b, task_a)
    finally:
        cleanup_project_web_data(task_api, project_api, task_records, project_ids)
