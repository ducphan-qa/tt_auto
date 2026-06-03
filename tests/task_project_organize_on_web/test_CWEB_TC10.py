import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.project_web_helpers import (
    cleanup_project_web_data,
    create_api_project,
    open_project_web,
    verify_selected_project,
)
from pages.helper.regression_helpers import unique_text

"""test_CWEB_TC10 - Verify Unicode project name appears and selects."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_CWEB_TC10")
@pytest.mark.tc_title("Verify project with Unicode name appears and can be selected.")
def test_verify_unicode_project_name_selects(api_request_context, authenticated_page):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []
    project_name = unique_text("PROJ WEB Unicode") + " \u0e17\u0e14\u0e2a\u0e2d\u0e1a"

    try:
        project_id = create_api_project(project_api, project_name)
        project_ids.append(project_id)
        open_project_web(authenticated_page)
        verify_selected_project(authenticated_page, project_name)
    finally:
        cleanup_project_web_data(task_api, project_api, task_records, project_ids)
