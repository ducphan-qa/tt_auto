from playwright.sync_api import Page, expect

from pages.helper.regression_helpers import (
    delete_project_if_exists,
    delete_task_if_exists,
)
from pages.web import config
from pages.web.locators.detail_view import DetailViewElements
from pages.web.locators.project_list_scroller_elements import (
    ProjectListScrollerElements,
)
from pages.web.locators.task_list_view_elements import TaskListViewElements
from pages.web.login_page import LoginPage
from pages.web.side_bar import SideBar
from pages.web.view_contents import ViewContents


def open_project_web(page: Page) -> Page:
    page.goto(config.TICKTICK_URL_WEBAPP)
    LoginPage(page).assert_app_loaded()
    return page


def create_api_project(project_api, project_name, color=None):
    body = {
        "name": project_name,
        "viewMode": "list",
        "kind": "TASK",
    }
    if color is not None:
        body["color"] = color

    created_project = project_api.create_project(body)
    assert created_project is not None, "Create project response is empty"
    assert "id" in created_project, f"Project id missing: {created_project}"
    return created_project["id"]


def update_api_project(project_api, project_id, project_name, color=None):
    body = {
        "name": project_name,
        "viewMode": "list",
        "kind": "TASK",
    }
    if color is not None:
        body["color"] = color

    updated_project = project_api.update_project(project_id, body)
    assert updated_project is not None, "Update project response is empty"
    assert updated_project["id"] == project_id
    assert updated_project["name"] == project_name
    return updated_project


def create_api_task(task_api, project_id, task_title, task_content):
    created_task = task_api.create_task(
        task_title=task_title,
        task_content=task_content,
        project_id=project_id,
    )
    assert created_task is not None, "Create task response is empty"
    assert "id" in created_task, f"Task id missing: {created_task}"
    return created_task["id"]


def cleanup_project_web_data(task_api, project_api, task_records, project_ids):
    for task_id, project_id in reversed(task_records):
        delete_task_if_exists(task_api, task_id, project_id)

    for project_id in reversed(project_ids):
        delete_project_if_exists(project_api, project_id)


def verify_project_list_visible(page: Page) -> None:
    SideBar(page).verify_project_list_visible()
    project_scroller = ProjectListScrollerElements(page)
    expect(project_scroller.project_list).to_be_visible()


def verify_smart_project_selectable(page: Page, name: str) -> None:
    sidebar = SideBar(page)
    sidebar.verify_smart_project_visible(name)
    sidebar.select_smart_project(name)
    expect(TaskListViewElements(page).root).to_be_visible()


def verify_project_visible(page: Page, project_name: str) -> None:
    project_scroller = ProjectListScrollerElements(page)
    expect(project_scroller.project_button_by_name(project_name)).to_be_visible(
        timeout=30000
    )


def select_project(page: Page, project_name: str) -> None:
    view = ViewContents(page)
    view.select_project(project_name)


def verify_selected_project(page: Page, project_name: str) -> None:
    select_project(page, project_name)
    expect(TaskListViewElements(page).project_title).to_contain_text(
        project_name,
        timeout=15000,
    )


def verify_project_task_visible(page: Page, project_name: str, task_title: str) -> None:
    view = ViewContents(page)
    view.select_project(project_name)
    view.verify_task_visible(task_title)


def verify_project_tasks_visible(
    page: Page,
    project_name: str,
    task_titles: list[str],
) -> None:
    ViewContents(page).verify_project_tasks_visible(project_name, task_titles)


def verify_task_not_visible(page: Page, project_name: str, task_title: str) -> None:
    select_project(page, project_name)
    expect(TaskListViewElements(page).body.get_by_text(task_title, exact=True)).to_be_hidden(
        timeout=5000
    )


def verify_empty_project_view(page: Page, project_name: str) -> None:
    select_project(page, project_name)
    task_list = TaskListViewElements(page)
    expect(task_list.quick_add).to_be_visible()
    expect(task_list.body).to_be_visible()


def verify_task_detail_project_association(
    page: Page,
    project_name: str,
    task_title: str,
    task_content: str,
) -> None:
    view = ViewContents(page)
    view.verify_project_task_contents(project_name, task_title, task_content)
    detail = DetailViewElements(page)
    expect(detail.root.get_by_text(project_name).first).to_be_visible(timeout=15000)


def verify_project_row_still_visible_after_tasks(
    page: Page,
    project_name: str,
    task_titles: list[str],
) -> None:
    verify_project_visible(page, project_name)
    verify_project_tasks_visible(page, project_name, task_titles)
    verify_project_visible(page, project_name)


def verify_project_navigation_keeps_shell_visible(page: Page, project_name: str) -> None:
    select_project(page, project_name)
    SideBar(page).verify_sidebar_sections_visible()
    expect(TaskListViewElements(page).quick_add).to_be_visible()
