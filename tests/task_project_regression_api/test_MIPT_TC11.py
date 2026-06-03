import pytest

from pages.api.project_organize import ProjectOrganize
from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import (
    assert_task_values,
    create_task,
    create_temp_project,
    delete_project_if_exists,
    delete_task_if_exists,
)

"""test_MIPT_TC11 - Move task to another project updates visibility."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_MIPT_TC11")
@pytest.mark.tc_title("Move task to another project updates visibility.")
def test_move_task_to_another_project_updates_visibility(api_request_context):
    project = ProjectOrganize(api_request_context)
    task = TaskOrganize(api_request_context)
    source_project_id = task.project_id_default
    target_project_id = None
    task_id = None
    task_moved = False

    try:
        target_project_id = create_temp_project(project, "REG011 Target Project")
        created_task, title, content = create_task(
            task, "REG011", project_id=source_project_id
        )
        task_id = created_task["id"]

        move_response = task.move_task(source_project_id, target_project_id, task_id)
        assert move_response is not None, "Move response is empty"
        assert move_response.status == 200
        task_moved = True

        target_detail = task.get_task(task_id=task_id, project_id=target_project_id)
        assert_task_values(target_detail, task_id, target_project_id, title, content)

        source_detail = task.get_task(
            task_id=task_id,
            project_id=source_project_id,
            expected_status=404,
        )
        assert source_detail is None
    finally:
        delete_task_if_exists(
            task, task_id, target_project_id if task_moved else source_project_id
        )
        delete_project_if_exists(project, target_project_id)
