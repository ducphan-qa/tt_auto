import pytest
"""test_VWEB_TC22 - Verify TickTick web locator root elements"""

from playwright.sync_api import expect

from pages.web import config
from pages.web.locators.detail_view import DetailViewElements
from pages.web.locators.project_list_scroller_elements import (
    ProjectListScrollerElements,
)
from pages.web.locators.sidebar_elements import SidebarElements
from pages.web.locators.task_list_view_elements import TaskListViewElements
from pages.web.login_page import LoginPage


@pytest.mark.tc_id("test_VWEB_TC22")
@pytest.mark.tc_title("Verify TickTick web locator root elements")
def test_ticktick_web_locator_roots(authenticated_page):
    authenticated_page.goto(config.TICKTICK_URL_WEBAPP)
    LoginPage(authenticated_page).assert_app_loaded()

    sidebar = SidebarElements(authenticated_page)
    project_scroller = ProjectListScrollerElements(authenticated_page)
    task_list = TaskListViewElements(authenticated_page)
    detail_view = DetailViewElements(authenticated_page)

    expect(sidebar.root).to_be_visible()
    expect(project_scroller.root).to_be_visible()
    expect(task_list.root).to_be_visible()
    expect(detail_view.root).to_be_attached()

    expect(project_scroller.smart_project_by_name("Inbox")).to_be_visible()
    expect(task_list.header).to_be_visible()
    expect(task_list.quick_add).to_be_visible()
    expect(detail_view.wrapper).to_be_attached()
