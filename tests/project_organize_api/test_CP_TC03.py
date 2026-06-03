from pages.api.project_organize import ProjectOrganize
from pages.api.verify_funtions import VerifyFunctions
import logging
import pytest

""" P03 - Create Kanban TASK project"""

project_name = "API Test Project"
project_color = "#F18181"
view_mode = "kanban"
kind = "TASK"


@pytest.mark.api
@pytest.mark.sanity
@pytest.mark.tc_id("test_CP_TC03")
@pytest.mark.tc_title("Create Kanban TASK project")
def test_create_get_delete_project_with_normal_text(api_request_context):

    verify = VerifyFunctions()

    # Create project
    body = {
        "name": project_name,
        "color": project_color,
        "viewMode": view_mode,
        "kind": kind,
    }

    create_project = ProjectOrganize(api_request_context)

    response = create_project.create_project(body)

    if not response or "id" not in response:
        logging.error(
            f"Create project failed or project id not found. Response: {response}"
        )
        return

    verify.assert_value_of_key_in_json(response, body)

    # Get project

    project_id = response["id"]
    get_response = create_project.get_project_by_id(project_id)
    verify.assert_value_of_key_in_json(get_response, body)

    # Delete project

    delete_response = create_project.delele_project(project_id)
