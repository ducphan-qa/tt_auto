from pages.api.task_organize import TaskOrganize
import logging
import pytest

"""test_CT_TC03 - Create/Get/Delete Task With Long Text"""

# Values
current_task_title = (
    "Automation Regression Suite Execution Report - Sprint 25 Build Validation"
)
current_task_content = "Execute smoke, sanity, regression, API validation, performance baseline, and certificate authentication validation for pre-production environment."


@pytest.mark.api
@pytest.mark.sanity
@pytest.mark.tc_id("test_CT_TC03")
@pytest.mark.tc_title("Create/Get/Delete Task With Long Text")
def test_create_get_delete_task_with_long_text(
    api_request_context,
):

    # Create task
    create_task = TaskOrganize(api_request_context)

    response = create_task.create_task(
        task_title=current_task_title, task_content=current_task_content
    )

    task_id = response["id"]
    logging.info(f"Created task ID is: {task_id}")

    # Verify created task

    task_detail = create_task.get_task(task_id=task_id)
    assert task_detail["id"] == task_id  # type: ignore
    assert task_detail["title"] == current_task_title  # type: ignore
    assert task_detail["content"] == current_task_content  # type: ignore

    # Delete task
    create_task.delete_task(task_id=task_id)

    # Verify deleted task
    create_task.get_task(task_id=task_id, expected_status=404)
