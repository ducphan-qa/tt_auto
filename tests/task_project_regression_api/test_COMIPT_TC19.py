import pytest

"""test_COMIPT_TC19 - Comments bind to task within project."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.xfail(reason="TickTick Open API v1 does not expose task comment endpoints.")
@pytest.mark.tc_id("test_COMIPT_TC19")
@pytest.mark.tc_title("Comments bind to task within project.")
def test_comments_bind_to_task_within_project(api_request_context):
    assert False, "No official TickTick Open API v1 comment endpoint is available"
