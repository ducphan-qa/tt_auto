from playwright.sync_api import Locator, Page


class TaskListViewElements:
    """Locators for the center TickTick task list view."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.root = page.locator("#task-list-view")

    @property
    def header(self) -> Locator:
        return self.root.locator("header.tl-bar").first

    @property
    def sidebar_toggle_button(self) -> Locator:
        return self.root.locator("#left-menu-t")

    @property
    def project_name_bar(self) -> Locator:
        return self.root.locator("#project-name-bar")

    @property
    def project_title(self) -> Locator:
        return self.project_name_bar.locator(".tl-bar-project-name, span, div").first

    @property
    def action_bar(self) -> Locator:
        return self.root.locator(".tl-bar-action-bar").first

    @property
    def action_buttons(self) -> Locator:
        return self.action_bar.locator("button, a")

    @property
    def more_button(self) -> Locator:
        return self.action_buttons.last

    @property
    def quick_add(self) -> Locator:
        return self.root.locator("#add-task, .task-input").first

    @property
    def add_task_textarea(self) -> Locator:
        return self.quick_add.locator("textarea").first

    @property
    def add_task_placeholder(self) -> Locator:
        return self.quick_add.locator(".fake-placeholder").first

    @property
    def body(self) -> Locator:
        return self.root.locator("#task-list-body")

    @property
    def empty_state(self) -> Locator:
        return self.body.locator(".empty-list-info").first

    @property
    def task_rows(self) -> Locator:
        return self.body.locator(
            "[data-task-id], .task-item, .tasklist-item, [class*='task-row' i]"
        )

    @property
    def task_checkboxes(self) -> Locator:
        return self.body.locator(
            "[role='checkbox'], input[type='checkbox'], [class*='checkbox' i]"
        )

    def task_by_title(self, title: str) -> Locator:
        return self.task_rows.filter(has_text=title).first

    def task_checkbox_by_title(self, title: str) -> Locator:
        return self.task_by_title(title).locator(
            "[role='checkbox'], input[type='checkbox'], [class*='checkbox' i]"
        ).first

    def toolbar_button_by_label(self, label: str) -> Locator:
        return self.action_bar.locator(
            f"button[aria-label*='{label}' i], a[aria-label*='{label}' i]"
        ).first
