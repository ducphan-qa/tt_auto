import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.project_web_helpers import (
    cleanup_project_web_data,
    create_api_project,
    open_project_web,
    verify_empty_project_view,
)
from pages.helper.regression_helpers import unique_text

"""test_CWEB_TC08 - Verify empty API-created project shows project task area."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_CWEB_TC08")
@pytest.mark.tc_title("Verify API-created empty project shows selected project task area.")
def test_verify_empty_api_created_project_shows_task_area(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []
    project_name = unique_text("PROJ WEB Empty")

    try:
        project_id = create_api_project(project_api, project_name)
        project_ids.append(project_id)
        open_project_web(authenticated_page)
        verify_empty_project_view(authenticated_page, project_name)
    finally:
        cleanup_project_web_data(task_api, project_api, task_records, project_ids)
