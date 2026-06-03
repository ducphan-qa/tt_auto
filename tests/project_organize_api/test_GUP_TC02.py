import pytest

from pages.api.project_organize import ProjectOrganize

"""TC02 - Get all user projects successfully"""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_GUP_TC02")
@pytest.mark.tc_title("Get all user projects successfully")
def test_get_all_user_projects_successfully(api_request_context):
    project = ProjectOrganize(api_request_context)

    projects = project.get_user_project()

    assert projects is not None, "Get all projects response is empty"
    assert isinstance(projects, list), f"Expected project list but got {type(projects)}"
    assert len(projects) > 0, "Expected at least one project"

    for project_item in projects:
        assert "id" in project_item, f"Project id not found: {project_item}"
        assert "name" in project_item, f"Project name not found: {project_item}"
