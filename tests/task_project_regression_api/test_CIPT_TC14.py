import pytest

from pages.api.task_organize import TaskOrganize
from pages.helper.regression_helpers import delete_task_if_exists, unique_text

"""test_CIPT_TC14 - Batch add workflow creates tasks under same project."""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.tc_id("test_CIPT_TC14")
@pytest.mark.tc_title("Batch add workflow creates tasks under same project.")
def test_batch_add_workflow_creates_tasks_under_same_project(api_request_context):
    task = TaskOrganize(api_request_context)
    project_id = task.project_id_default
    created_task_ids = []

    try:
        payloads = [
            {
                "title": unique_text(f"REG014 Batch Add {index}"),
                "content": unique_text(f"REG014 Batch Content {index}"),
                "projectId": project_id,
            }
            for index in range(1, 4)
        ]
        created_tasks = task.batch_add_tasks(payloads)
        assert created_tasks is not None, "Batch add response is empty"
        assert len(created_tasks) == len(payloads)
        created_task_ids = [item["id"] for item in created_tasks]

        for payload, created_task in zip(payloads, created_tasks):
            task_detail = task.get_task(task_id=created_task["id"], project_id=project_id)
            assert task_detail["projectId"] == project_id
            assert task_detail["title"] == payload["title"]
            assert task_detail.get("content", "") == payload["content"]
    finally:
        for task_id in created_task_ids:
            delete_task_if_exists(task, task_id, project_id)
