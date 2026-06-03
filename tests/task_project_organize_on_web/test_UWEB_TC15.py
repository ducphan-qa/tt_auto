import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.project_web_helpers import (
    cleanup_project_web_data,
    create_api_project,
    open_project_web,
    update_api_project,
    verify_selected_project,
)
from pages.helper.regression_helpers import unique_text

"""test_UWEB_TC15 - Verify API-renamed project appears on web after reload."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_UWEB_TC15")
@pytest.mark.tc_title("Verify API-renamed project appears on web after reload.")
def test_verify_api_renamed_project_appears_after_reload(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []
    original_name = unique_text("PROJ WEB Rename Original")
    renamed_name = unique_text("PROJ WEB Rename Updated")

    try:
        project_id = create_api_project(project_api, original_name)
        project_ids.append(project_id)
        update_api_project(project_api, project_id, renamed_name)
        open_project_web(authenticated_page)
        verify_selected_project(authenticated_page, renamed_name)
    finally:
        cleanup_project_web_data(task_api, project_api, task_records, project_ids)
