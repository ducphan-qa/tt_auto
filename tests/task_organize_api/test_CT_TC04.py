from pages.api.task_organize import TaskOrganize
import logging
import pytest

"""TC04 — Create/Get/Delete Task With Unicode and Multi-language Content"""

# Values
current_task_title = "测试任务_日本語_Vietnamese"
current_task_content = "Xin chào 🚀 こんにちは 세계 안녕"


@pytest.mark.api
@pytest.mark.sanity
@pytest.mark.tc_id("test_CT_TC04")
@pytest.mark.tc_title("Create/Get/Delete Task With Unicode and Multi-language Content")
def test_create_get_delete_task_with_unicode_and_multi_language_content(
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
