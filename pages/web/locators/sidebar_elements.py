from playwright.sync_api import Locator, Page


class SidebarElements:
    """Locators for TickTick's left sidebar shell."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.root = page.locator("#project-list-view, #leftListView").first

    @property
    def project_scroller(self) -> Locator:
        return self.page.locator("#project-list-scroller")

    @property
    def smart_projects_area(self) -> Locator:
        return self.root.locator("#smart-project-view-area")

    @property
    def today(self) -> Locator:
        return self.root.locator("#smart-project-today").first

    @property
    def inbox(self) -> Locator:
        return self.root.locator("#smart-project-inbox").first

    @property
    def next_7_days(self) -> Locator:
        return self.smart_project_by_name("Next 7 Days")

    @property
    def completed(self) -> Locator:
        return self.smart_project_by_name("Completed")

    @property
    def trash(self) -> Locator:
        return self.smart_project_by_name("Trash")

    @property
    def section_headers(self) -> Locator:
        return self.root.locator(".project-list")

    @property
    def lists_section(self) -> Locator:
        return self.section_by_name("Lists")

    @property
    def filters_section(self) -> Locator:
        return self.section_by_name("Filters")

    @property
    def tags_section(self) -> Locator:
        return self.section_by_name("Tags")

    def section_by_name(self, name: str) -> Locator:
        return self.section_headers.filter(has_text=name).or_(
            self.root.get_by_text(name, exact=True)
        ).first

    def smart_project_by_name(self, name: str) -> Locator:
        return self.root.locator(".smart-project-dropper").filter(has_text=name).first

    def navigation_item_by_name(self, name: str) -> Locator:
        return self.root.locator(".project-list-view-item-button").filter(
            has_text=name
        ).first
