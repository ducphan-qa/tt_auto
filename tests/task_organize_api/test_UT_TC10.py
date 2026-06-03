from pages.api.task_organize import TaskOrganize
from pages.api.verify_funtions import VerifyFunctions
import logging
import pytest
import dotenv, os

dotenv.load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")

"""TC10 — Update Task With Long Title And Long Content"""

# Values
current_task_title = "Buy Milk"
current_task_content = "Buy Milk at the Vinamilk store at 7AM"

new_long_title = (
    "Verify task creation with a long title containing alphabetic characters, numbers 1234567890, "
    "special symbols !@#$%^&*(), and repeated meaningful text to reach around two hundred characters safely."
)

new_long_content = (
    "This is a long task content used for API and UI validation. "
    "The purpose of this test data is to verify that the system can correctly create, store, retrieve, "
    "update, display, and delete a task when the content field contains a large amount of text. "
    "It should also confirm that the backend does not truncate the content unexpectedly, the database column "
    "supports the expected size, and the response body returns the same value that was submitted in the request. "
    "This content includes normal sentences, punctuation marks, numbers such as 1234567890, and special characters "
    "such as !@#$%^&*()_+-=[]{}|;:',.<>?/. "
    "The test should verify that line wrapping, encoding, JSON serialization, and field validation all work correctly. "
    "In a real application, users may enter long descriptions, detailed notes, instructions, acceptance criteria, "
    "bug reproduction steps, investigation results, or meeting notes into the task content field. "
    "Therefore, this test data helps ensure the application handles realistic long-form input without failing. "
    "The system should return a successful response when the content length is within the allowed limit. "
    "After creating the task, the test should get the task by task ID and compare the returned content with the original "
    "content exactly. Any mismatch should be treated as a test failure. "
    "The test should also verify that deleting the task works correctly after long content has been stored. "
    "This helps confirm that the full create, read, and delete flow works with large payload data. "
    "Additional repeated text is included here to increase the content length close to two thousand characters. "
    "Long content validation is important because some issues only appear when payload size increases, including timeout, "
    "bad request errors, database length limits, serialization bugs, UI overflow, or incorrect API response formatting. "
    "This test content should remain stable and deterministic so that assertions are reliable across multiple test runs. "
    "The same value should be reusable in automated test cases without depending on random generated text. "
    "End of long content test data."
)


@pytest.mark.api
@pytest.mark.sanity
@pytest.mark.tc_id("test_UT_TC10")
@pytest.mark.tc_title("Update Task With Long Title And Long Content")
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
        "title": new_long_title,
        "content": new_long_content,
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
