from pages.api.project_organize import ProjectOrganize
from pages.api.verify_funtions import VerifyFunctions
import logging
import pytest

"""P04 - Create Timeline TASK project with sortOrder"""

project_name = "P04 - Create Timeline TASK project with sortOrder"
project_color = "#7CB342"
sort_order = 1000
view_mode = "timeline"
kind = "TASK"


@pytest.mark.api
@pytest.mark.sanity
@pytest.mark.tc_id("test_CP_TC04")
@pytest.mark.tc_title("Create Timeline TASK project with sortOrder")
def test_create_get_delete_project_with_normal_text(api_request_context):

    verify = VerifyFunctions()

    # Create project
    body = {
        "name": project_name,
        "color": project_color,
        "sortOrder": sort_order,
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
