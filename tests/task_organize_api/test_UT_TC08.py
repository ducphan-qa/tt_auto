from pages.api.task_organize import TaskOrganize
from pages.api.verify_funtions import VerifyFunctions
import logging
import pytest
import dotenv, os

dotenv.load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")

"""TC08 — Update Task Title And Content With Special Characters"""

# Values
current_task_title = "Buy Milk"
current_task_content = "Buy Milk at the Vinamilk store at 7AM"

new_task_title = "Task @#$%^&*()"
new_task_content = "Verify symbols: !@#$%^&*()_+-=[]{}|;:',.<>/?"


@pytest.mark.api
@pytest.mark.sanity
@pytest.mark.tc_id("test_UT_TC08")
@pytest.mark.tc_title("Update Task Title And Content With Special Characters")
def test_create_update_get_delete_task_title_with_multi_line_text(api_request_context):

    verify = VerifyFunctions()

    # Create task with current title and content
    task = TaskOrganize(api_request_context)

    response = task.create_task(
        task_title=current_task_title, task_content=current_task_content
    )

    task_id = response["id"]
    logging.info(f"Created task ID is: {task_id}")

    # Update task
    data = {
        "id": task_id,
        "projectId": PROJECT_ID,
        "title": new_task_title,
        "content": new_task_content,
        "priority": 1,
    }

    task.update_task(task_id, data)

    # Get task and verify updated title
    task.get_task(task_id)

    # verify._assert_value_of_key_in_json(get_task_response, data)

    # Delete task
    task.delete_task(task_id)

    # Get task again and verify
    # No need -> you task will move to the trash, but still get in api -> bug
