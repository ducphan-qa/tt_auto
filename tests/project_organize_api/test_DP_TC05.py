from datetime import datetime

import pytest

from pages.api.project_organize import ProjectOrganize

"""TC05 - Delete project successfully"""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_DP_TC05")
@pytest.mark.tc_title("Delete project successfully")
def test_delete_project_successfully(api_request_context):
    project = ProjectOrganize(api_request_context)

    project_id = None
    project_deleted = False

    try:
        project_name = (
            "TC05 - Project Delete "
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

        delete_response = project.delele_project(project_id)
        assert delete_response is not None, "Delete project response is empty"
        assert delete_response.status == 200, (
            f"Expected delete status 200 but got {delete_response.status}"
        )
        project_deleted = True

        deleted_project_detail = project.get_project_by_id(
            project_id,
            expected_status=404,
        )
        assert deleted_project_detail is None, "Deleted project is still retrievable"

        projects = project.get_user_project()
        assert projects is not None, "Get all projects response is empty"
        project_ids = [project_item.get("id") for project_item in projects]
        assert project_id not in project_ids, "Deleted project still appears in list"

    finally:
        if project_id and not project_deleted:
            project.delele_project(project_id)
