from datetime import datetime

import pytest

from pages.api.project_organize import ProjectOrganize

"""TC04 - Update project successfully"""

updated_color = "#5E97F6"


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_UP_TC04")
@pytest.mark.tc_title("Update project successfully")
def test_update_project_successfully(api_request_context):
    project = ProjectOrganize(api_request_context)

    project_id = None

    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        project_body = {
            "name": f"TC04 - Project Before Update {timestamp}",
            "color": "#F18181",
            "viewMode": "list",
            "kind": "TASK",
        }

        created_project = project.create_project(project_body)
        assert created_project is not None, "Create project failed"
        assert "id" in created_project, (
            f"Project id not found. Response: {created_project}"
        )
        project_id = created_project["id"]

        update_body = {
            "name": f"Updated API Test Project {timestamp}",
            "color": updated_color,
            "viewMode": "list",
            "kind": "TASK",
        }
        updated_project = project.update_project(project_id, update_body)
        assert updated_project is not None, "Update project response is empty"
        assert updated_project["id"] == project_id
        assert updated_project["name"] == update_body["name"]
        assert updated_project["color"] == update_body["color"]

        project_detail = project.get_project_by_id(project_id)
        assert project_detail is not None, "Project detail response is empty"
        assert project_detail["id"] == project_id
        assert project_detail["name"] == update_body["name"]
        assert project_detail["color"] == update_body["color"]

    finally:
        if project_id:
            project.delele_project(project_id)
