from playwright.sync_api import Page, expect

from pages.web.locators.detail_view import DetailViewElements
from pages.web.locators.project_list_scroller_elements import (
    ProjectListScrollerElements,
)
from pages.web.locators.task_list_view_elements import TaskListViewElements


class ViewContents:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.project_scroller = ProjectListScrollerElements(page)
        self.task_list = TaskListViewElements(page)
        self.detail = DetailViewElements(page)

    def verify_project_task_contents(
        self,
        project_name: str,
        task_title: str,
        task_content: str | None,
    ) -> None:
        self.select_project(project_name)
        self.verify_task_detail(task_title, task_content)

    def verify_project_tasks_visible(
        self,
        project_name: str,
        task_titles: list[str],
    ) -> None:
        self.select_project(project_name)
        for task_title in task_titles:
            self.verify_task_visible(task_title)

    def select_project(self, project_name: str) -> None:
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.project_scroller.root).to_be_visible(timeout=30000)
        expect(self.task_list.root).to_be_visible(timeout=30000)

        project = self.project_scroller.project_button_by_name(project_name)
        expect(project).to_be_visible(timeout=30000)
        project.scroll_into_view_if_needed()
        project.click()

        expect(self.task_list.project_title).to_contain_text(
            project_name,
            timeout=15000,
        )

    def verify_task_visible(self, task_title: str) -> None:
        task_row = self._task_by_title(task_title)
        expect(task_row).to_be_visible(timeout=30000)

    def open_task(self, task_title: str) -> None:
        task_row = self._task_by_title(task_title)
        expect(task_row).to_be_visible(timeout=30000)
        task_row.scroll_into_view_if_needed()
        task_row.click()
        expect(self.detail.root).to_be_attached(timeout=15000)

    def verify_task_detail(self, task_title: str, task_content: str | None) -> None:
        self.open_task(task_title)
        self._expect_detail_value_or_text(task_title, "task title")
        if task_content is not None:
            self._expect_detail_value_or_text(task_content, "task content")

    def _expect_detail_value_or_text(self, expected_text: str, field_name: str) -> None:
        if "\n" in expected_text:
            for line in [item for item in expected_text.splitlines() if item]:
                self._expect_detail_value_or_text(line, field_name)
            return

        candidates = [
            self.detail.root.get_by_text(expected_text, exact=True).first,
            self.detail.title_editor,
            self.detail.description_editor,
            self.detail.root.locator(
                "textarea, input, [contenteditable='true'], .CodeMirror"
            ).filter(has_text=expected_text).first,
        ]

        for candidate in candidates:
            if self._matches_visible_text(candidate, expected_text):
                return
            if self._matches_value(candidate, expected_text):
                return

        raise AssertionError(f"Cannot find {field_name}: {expected_text}")

    def _task_by_title(self, title: str):
        return self.task_list.task_by_title(title).or_(
            self.task_list.body.get_by_text(title, exact=True)
        ).first

    def _matches_visible_text(self, locator, expected_text: str) -> bool:
        try:
            expect(locator).to_be_visible(timeout=3000)
            expect(locator).to_contain_text(expected_text, timeout=3000)
            return True
        except AssertionError:
            return False

    def _matches_value(self, locator, expected_text: str) -> bool:
        try:
            expect(locator).to_be_visible(timeout=3000)
            expect(locator).to_have_value(expected_text, timeout=3000)
            return True
        except AssertionError:
            return False
