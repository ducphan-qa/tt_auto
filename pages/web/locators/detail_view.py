from playwright.sync_api import Locator, Page


class DetailViewElements:
    """Locators for TickTick's right-side task detail view."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.root = page.locator("#detail-view, #right-view").first

    @property
    def wrapper(self) -> Locator:
        return self.root.locator(".detail-view-wrapper").first

    @property
    def title_editor(self) -> Locator:
        return self.root.locator(
            "textarea, input, [contenteditable='true'], .CodeMirror"
        ).first

    @property
    def description_editor(self) -> Locator:
        return self.root.locator(
            "[class*='desc' i] textarea, [class*='content' i] textarea, "
            "[class*='desc' i] [contenteditable='true'], "
            "[class*='content' i] [contenteditable='true']"
        ).first

    @property
    def close_button(self) -> Locator:
        return self.root.locator(
            "button[aria-label*='close' i], [class*='close' i]"
        ).first

    @property
    def more_button(self) -> Locator:
        return self.root.locator(
            "button[aria-label*='more' i], a[aria-label*='more' i], "
            "[class*='more' i]"
        ).first

    @property
    def due_date_control(self) -> Locator:
        return self.detail_field_by_label("Date")

    @property
    def priority_control(self) -> Locator:
        return self.detail_field_by_label("Priority")

    @property
    def tags_control(self) -> Locator:
        return self.detail_field_by_label("Tags")

    @property
    def project_control(self) -> Locator:
        return self.detail_field_by_label("List")

    @property
    def subtask_rows(self) -> Locator:
        return self.root.locator("[class*='subtask' i], [data-subtask-id]")

    @property
    def comment_or_activity_rows(self) -> Locator:
        return self.root.locator("[class*='comment' i], [class*='activity' i]")

    @property
    def attachment_controls(self) -> Locator:
        return self.root.locator(
            "input[type='file'], button[aria-label*='attach' i], "
            "[class*='attachment' i], [class*='file' i]"
        )

    def detail_field_by_label(self, label: str) -> Locator:
        return self.root.locator(
            f"[aria-label*='{label}' i], [title*='{label}' i]"
        ).first.or_(self.root.get_by_text(label, exact=True).first)
