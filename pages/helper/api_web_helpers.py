from pages.helper.regression_helpers import (
    delete_project_if_exists,
    delete_task_if_exists,
)
from pages.web import config
from pages.web.login_page import LoginPage
from pages.web.view_contents import ViewContents


def create_api_project(project_api, project_name):
    created_project = project_api.create_project(
        {
            "name": project_name,
            "viewMode": "list",
            "kind": "TASK",
        }
    )
    assert created_project is not None, "Create project response is empty"
    assert "id" in created_project, f"Project id missing: {created_project}"
    return created_project["id"]


def create_api_task(task_api, project_id, task_title, task_content, extra_fields=None):
    created_task = task_api.create_task(
        task_title=task_title,
        task_content=task_content,
        project_id=project_id,
        extra_fields=extra_fields,
    )
    assert created_task is not None, "Create task response is empty"
    assert "id" in created_task, f"Task id missing: {created_task}"
    return created_task["id"]


def open_web_view(authenticated_page):
    authenticated_page.goto(config.TICKTICK_URL_WEBAPP)
    LoginPage(authenticated_page).assert_app_loaded()
    return ViewContents(authenticated_page)


def cleanup_generated_data(task_api, project_api, task_records, project_ids):
    for task_id, project_id in reversed(task_records):
        delete_task_if_exists(task_api, task_id, project_id)

    for project_id in reversed(project_ids):
        delete_project_if_exists(project_api, project_id)
