from datetime import datetime


NEGATIVE_STATUSES = (400, 401, 403, 404, 500)
CLEANUP_STATUSES = (200, 400, 404, 500)


def unique_text(prefix):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix} {timestamp}"


def create_temp_project(project, prefix):
    body = {
        "name": unique_text(prefix),
        "viewMode": "list",
        "kind": "TASK",
    }
    created_project = project.create_project(body)
    assert created_project is not None, "Create temporary project failed"
    assert "id" in created_project, f"Project id missing: {created_project}"
    return created_project["id"]


def delete_project_if_exists(project, project_id):
    if project_id:
        project.delele_project(project_id)


def create_task(
    task,
    title_prefix,
    content_prefix="Regression content",
    project_id=None,
    extra_fields=None,
):
    title = unique_text(title_prefix)
    content = unique_text(content_prefix)
    created_task = task.create_task(
        task_title=title,
        task_content=content,
        project_id=project_id,
        extra_fields=extra_fields,
    )
    assert created_task is not None, "Create task failed"
    assert "id" in created_task, f"Task id missing: {created_task}"
    return created_task, title, content


def delete_task_if_exists(task, task_id, project_id=None):
    if task_id:
        task.delete_task(
            task_id=task_id,
            project_id=project_id,
            expected_status=CLEANUP_STATUSES,
        )


def assert_task_values(task_detail, task_id, project_id, title=None, content=None):
    assert task_detail is not None, "Task detail is empty"
    assert task_detail["id"] == task_id
    assert task_detail["projectId"] == project_id
    if title is not None:
        assert task_detail["title"] == title
    if content is not None:
        assert task_detail.get("content", "") == content


def assert_negative_task_response(response, message):
    if response is None:
        return

    assert not isinstance(response, dict), (
        f"{message}. Got successful task body: {response}"
    )
    assert response.status != 200, f"{message}. Got status 200"


def project_task_ids(project_data):
    return [item.get("id") for item in project_data.get("tasks", [])]
