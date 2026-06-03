from pages.api.task_organize import TaskOrganize
from pages.api.verify_funtions import VerifyFunctions
import logging
import pytest

"""TC01 — Create/Get/Delete Task With Normal Text"""

# Values
current_task_title = "Buy Milk"
current_task_content = "Go to supermarket at 7 PM"


@pytest.mark.api
@pytest.mark.sanity
@pytest.mark.tc_id("test_CT_TC01")
@pytest.mark.tc_title("Create/Get/Delete Task With Normal Text")
def test_create_get_delete_task_with_normal_text(api_request_context):

    verify_funtion = VerifyFunctions()

    # Create task
    create_task = TaskOrganize(api_request_context)

    response = create_task.create_task(
        task_title=current_task_title, task_content=current_task_content
    )

    if not response or "id" not in response:
        logging.error(
            f"Create project failed or project id not found. Response: {response}"
        )
        return

    task_id = response["id"]
    logging.info(f"Created task ID is: {task_id}")

    # Verify created task

    task_detail = create_task.get_task(task_id=task_id)

    # assert task_detail["id"] == task_id  # type: ignore
    # assert task_detail["title"] == current_task_title  # type: ignore
    # assert task_detail["content"] == current_task_content  # type: ignore

    verify_funtion._assert_value_of_key_in_json(
        task_detail,
        {
            "id": task_id,
            "title": current_task_title,
            "content": current_task_content,
        },
    )

    # Delete task
    create_task.delete_task(task_id=task_id)

    # Verify deleted task
    create_task.get_task(task_id=task_id, expected_status=404)
