import pytest

from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import (
    create_task,
    delete_task_if_exists,
    unique_text,
)

"""test_UIPT_TC15 - Batch update workflow preserves project ownership."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_UIPT_TC15")
@pytest.mark.tc_title("Batch update workflow preserves project ownership.")
def test_batch_update_workflow_preserves_project_ownership(api_request_context):
    task = TaskOrganize(api_request_context)
    project_id = task.project_id_default
    created_task_ids = []

    try:
        for index in range(1, 4):
            created_task, _, _ = create_task(task, f"REG015 Original {index}", project_id=project_id)
            created_task_ids.append(created_task["id"])

        update_payloads = [
            {
                "id": task_id,
                "projectId": project_id,
                "title": unique_text(f"REG015 Updated {index}"),
                "content": unique_text(f"REG015 Updated Content {index}"),
                "priority": 1,
            }
            for index, task_id in enumerate(created_task_ids, start=1)
        ]
        updated_tasks = task.batch_update_tasks(update_payloads)
        assert updated_tasks is not None, "Batch update response is empty"
        assert len(updated_tasks) == len(update_payloads)

        for payload in update_payloads:
            task_detail = task.get_task(task_id=payload["id"], project_id=project_id)
            assert task_detail["projectId"] == project_id
            assert task_detail["title"] == payload["title"]
            assert task_detail.get("content", "") == payload["content"]
            assert task_detail.get("priority") == payload["priority"]
    finally:
        for task_id in created_task_ids:
            delete_task_if_exists(task, task_id, project_id)
