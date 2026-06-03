from datetime import datetime

import pytest

from pages.api.project_organize import ProjectOrganize

"""TC03 - Get project by ID successfully"""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_GIDP_TC03")
@pytest.mark.tc_title("Get project by ID successfully")
def test_get_project_by_id_successfully(api_request_context):
    project = ProjectOrganize(api_request_context)

    project_id = None

    try:
        project_name = (
            "TC03 - Project Detail "
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        project_body = {
            "name": project_name,
            "viewMode": "list",
            "kind": "TASK",
        }

        created_project = project.create_project(project_body)
        assert created_project is not None, "Create project failed"
        assert "id" in created_project, (
            f"Project id not found. Response: {created_project}"
        )
        project_id = created_project["id"]

        project_detail = project.get_project_by_id(project_id)
        assert project_detail is not None, "Project detail response is empty"
        assert project_detail["id"] == project_id
        assert project_detail["name"] == project_name

    finally:
        if project_id:
            project.delele_project(project_id)
