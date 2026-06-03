from playwright.sync_api import Page, expect

from pages.web.locators.sidebar_elements import SidebarElements


class SideBar:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.elements = SidebarElements(page)

    def verify_sidebar_is_visible(self) -> None:
        expect(self.elements.root).to_be_visible()
        expect(self.elements.project_scroller).to_be_visible()

    def verify_project_list_visible(self) -> None:
        self.verify_sidebar_is_visible()
        expect(self.elements.lists_section).to_be_visible()

    def verify_smart_projects_visible(self) -> None:
        expect(self.elements.today).to_be_visible()
        expect(self.elements.next_7_days).to_be_visible()
        expect(self.elements.inbox).to_be_visible()
        expect(self.elements.completed).to_be_visible()
        expect(self.elements.trash).to_be_visible()

    def verify_smart_project_visible(self, name: str) -> None:
        expect(self._smart_project_locator(name)).to_be_visible()

    def select_smart_project(self, name: str) -> None:
        smart_project = self._smart_project_locator(name)
        expect(smart_project).to_be_visible()
        smart_project.click()

    def verify_sidebar_sections_visible(self) -> None:
        expect(self.elements.lists_section).to_be_visible()
        expect(self.elements.filters_section).to_be_visible()
        expect(self.elements.tags_section).to_be_visible()

    def verify_filters_and_tags_visible(self) -> None:
        expect(self.elements.filters_section).to_be_visible()
        expect(self.elements.tags_section).to_be_visible()

    def verify_navigation_item_visible(self, name: str) -> None:
        expect(self.elements.navigation_item_by_name(name)).to_be_visible()

    def verify_project_visible(self, name: str) -> None:
        expect(self.elements.navigation_item_by_name(name)).to_be_visible()

    def verify_all_sidebar_elements(self) -> None:
        self.verify_sidebar_is_visible()
        self.verify_smart_projects_visible()
        self.verify_sidebar_sections_visible()

    def _smart_project_locator(self, name: str):
        normalized_name = name.casefold()
        if normalized_name == "today":
            return self.elements.today
        if normalized_name == "next 7 days":
            return self.elements.next_7_days
        if normalized_name == "inbox":
            return self.elements.inbox
        if normalized_name == "completed":
            return self.elements.completed
        if normalized_name == "trash":
            return self.elements.trash
        return self.elements.smart_project_by_name(name)
