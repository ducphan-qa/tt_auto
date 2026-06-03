from playwright.sync_api import Locator, Page


class ProjectListScrollerElements:
    """Locators inside TickTick's project/list scroller."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.root = page.locator("#project-list-scroller")

    @property
    def smart_projects_area(self) -> Locator:
        return self.root.locator("#smart-project-view-area")

    @property
    def smart_project_rows(self) -> Locator:
        return self.root.locator(".smart-project-dropper")

    @property
    def project_list(self) -> Locator:
        return self.root.locator("#project-ul")

    @property
    def project_rows(self) -> Locator:
        return self.root.locator("#project-ul .project-dropper")

    @property
    def project_buttons(self) -> Locator:
        return self.root.locator(".project-list-view-item-button")

    @property
    def section_headers(self) -> Locator:
        return self.root.locator(".project-list")

    @property
    def add_list_button(self) -> Locator:
        return self.section_by_name("Lists").locator("button.add-icon").first

    @property
    def filter_more_button(self) -> Locator:
        return self.section_by_name("Filters").locator("button.more-icon").first

    @property
    def add_filter_button(self) -> Locator:
        return self.section_by_name("Filters").locator("button.add-icon").first

    @property
    def tag_more_button(self) -> Locator:
        return self.section_by_name("Tags").locator("button.more-icon").first

    @property
    def add_tag_button(self) -> Locator:
        return self.section_by_name("Tags").locator("button.add-icon").first

    def section_by_name(self, name: str) -> Locator:
        return self.section_headers.filter(has_text=name).first

    def smart_project_by_name(self, name: str) -> Locator:
        return self.smart_project_rows.filter(has_text=name).first

    def project_by_name(self, name: str) -> Locator:
        return self.project_rows.filter(has_text=name).first

    def project_button_by_name(self, name: str) -> Locator:
        return self.project_buttons.filter(has_text=name).first
