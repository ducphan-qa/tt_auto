import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.project_web_helpers import (
    cleanup_project_web_data,
    create_api_project,
    create_api_task,
    open_project_web,
    verify_task_detail_project_association,
)
from pages.helper.regression_helpers import unique_text

"""test_GWEB_TC12 - Verify task detail shows correct project association."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_GWEB_TC12")
@pytest.mark.tc_title("Verify project task detail shows the correct project association.")
def test_verify_task_detail_project_association(
    api_request_context,
    authenticated_page,
):
    project_api = ProjectOrganize(api_request_context)
    task_api = TaskOrganize(api_request_context)
    project_ids = []
    task_records = []
    project_name = unique_text("PROJ WEB Detail Project")
    task_title = unique_text("PROJ WEB Detail Task")
    task_content = unique_text("PROJ WEB Detail Content")

    try:
        project_id = create_api_project(project_api, project_name)
        project_ids.append(project_id)
        task_id = create_api_task(task_api, project_id, task_title, task_content)
        task_records.append((task_id, project_id))
        open_project_web(authenticated_page)
        verify_task_detail_project_association(
            authenticated_page,
            project_name,
            task_title,
            task_content,
        )
    finally:
        cleanup_project_web_data(task_api, project_api, task_records, project_ids)
