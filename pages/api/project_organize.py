from pages.api.verify_funtions import VerifyFunctions
from playwright.sync_api import APIRequestContext
import logging
import time

BASE_PATH = "/open/v1"


class ProjectOrganize:
    def __init__(self, api_request_context: APIRequestContext) -> None:
        self.request = api_request_context

        self.verify_funtion = VerifyFunctions()

    def _response_is_rate_limited(self, response):
        if response.status != 500:
            return False
        return "exceed_query_limit" in self.verify_funtion._get_response_text(response)

    def _send_request(self, method_name, path, retries=2, **kwargs):
        for attempt in range(retries + 1):
            response = getattr(self.request, method_name)(path, **kwargs)
            if not self._response_is_rate_limited(response) or attempt == retries:
                return response

            logging.info(
                "TickTick query rate limit reached. Waiting 65 seconds before retry."
            )
            time.sleep(65)

        return response

    def get_user_project(self):
        try:
            logging.info("Sending GET request to fetch all projects")
            response = self._send_request("get", f"{BASE_PATH}/project")
            self.verify_funtion.assert_status(response, 200)
            self.verify_funtion.assert_json_not_empty(response)

            if response.status == 200:
                response_json = response.json()
                logging.debug("Total projects returned: %s", len(response_json))
                return response_json

            logging.error(
                "Cannot fetch all projects. Status: %s.",
                response.status,
            )
            return None
        except Exception as error:
            logging.error("Unexpected error while fetching all projects: %s", error)
            return None

    def get_project_by_id(self, project_id, expected_status: int = 200):
        try:
            logging.info("Sending GET request to fetch project ID: %s", project_id)
            response = self._send_request("get", f"{BASE_PATH}/project/{project_id}")

            if expected_status == 404:
                if response.status == 404:
                    logging.info("Project ID %s returned 404 as expected", project_id)
                    return None

                if response.status == 200:
                    response_text = self.verify_funtion._get_response_text(response)
                    if not response_text.strip():
                        logging.info(
                            "Project ID %s returned 200 with empty body while "
                            "expected 404. Treating as not found.",
                            project_id,
                        )
                        return None

                    logging.info(
                        "Project ID %s is still retrievable after delete.",
                        project_id,
                    )
                    return response.json()

                logging.error(
                    "Cannot verify deleted project ID %s. Expected status: 404. "
                    "Actual status: %s.",
                    project_id,
                    response.status,
                )
                return None

            self.verify_funtion.assert_status(response, expected_status)

            if response.status == 200 and expected_status == 200:
                self.verify_funtion.assert_json_not_empty(response)
                response_json = response.json()
                logging.debug("Project ID is: %s", response_json.get("id"))
                logging.debug("Project color is: %s", response_json.get("color"))
                logging.debug("Project kind is: %s", response_json.get("kind"))
                return response_json

            logging.error(
                "Cannot fetch project ID %s. Expected status: %s. Actual status: "
                "%s.",
                project_id,
                expected_status,
                response.status,
            )
            return None
        except Exception as error:
            logging.error(
                "Unexpected error while fetching project ID %s: %s",
                project_id,
                error,
            )
            return None

    def get_project_with_data(self, project_id):
        try:
            logging.info("Sending GET request to fetch project data ID: %s", project_id)
            response = self._send_request(
                "get",
                f"{BASE_PATH}/project/{project_id}/data",
            )

            self.verify_funtion.assert_status(response, 200)
            self.verify_funtion.assert_json_not_empty(response)

            if response.status == 200:
                response_json = response.json()
                logging.debug("Project data ID is: %s", response_json.get("id"))
                logging.debug("Project data name is: %s", response_json.get("name"))
                logging.debug("Project data color is: %s", response_json.get("color"))
                logging.debug("Project data kind is: %s", response_json.get("kind"))
                return response_json

            logging.error(
                "Cannot fetch project data ID %s. Status: %s.",
                project_id,
                response.status,
            )
            return None
        except Exception as error:
            logging.error(
                "Unexpected error while fetching project data ID %s: %s",
                project_id,
                error,
            )
            return None

    def create_project(self, body):
        try:
            logging.info("Sending POST request to create project")
            logging.debug("Create project request includes keys: %s", sorted(body.keys()))
            response = self._send_request("post", f"{BASE_PATH}/project", data=body)

            self.verify_funtion.assert_status(response, 200)
            self.verify_funtion.assert_json_not_empty(response)

            if response.status == 200:
                response_json = response.json()
                logging.debug("Created project ID is: %s", response_json.get("id"))
                logging.debug(
                    "Created project color is: %s", response_json.get("color")
                )
                logging.debug("Created project kind is: %s", response_json.get("kind"))
                return response_json

            logging.error(
                "Cannot create project. Status: %s.",
                response.status,
            )
            return None
        except Exception as error:
            logging.error("Unexpected error while creating project: %s", error)
            return None

    def update_project(self, project_id, body, expected_status: int = 200):
        try:
            logging.info("Sending POST request to update project ID: %s", project_id)
            logging.debug("Update project request includes keys: %s", sorted(body.keys()))
            response = self._send_request(
                "post",
                f"{BASE_PATH}/project/{project_id}",
                data=body,
            )

            self.verify_funtion.assert_status(response, expected_status)

            if response.status == 200 and expected_status == 200:
                self.verify_funtion.assert_json_not_empty(response)
                response_json = response.json()
                logging.debug("Updated project ID is: %s", response_json.get("id"))
                logging.debug("Updated project color is: %s", response_json.get("color"))
                logging.debug("Updated project kind is: %s", response_json.get("kind"))
                return response_json

            logging.error(
                "Cannot update project ID %s. Expected status: %s. Actual status: "
                "%s.",
                project_id,
                expected_status,
                response.status,
            )
            return None
        except Exception as error:
            logging.error(
                "Unexpected error while updating project ID %s: %s",
                project_id,
                error,
            )
            return None

    def delele_project(self, project_id):
        try:
            logging.info("Sending DELETE request to delete project ID: %s", project_id)
            response = self._send_request("delete", f"{BASE_PATH}/project/{project_id}")

            self.verify_funtion.assert_status(response, 200)

            if response.status == 200:
                logging.info("Successfully deleted project ID: %s", project_id)
                return response

            logging.error(
                "Cannot delete project ID %s. Status: %s.",
                project_id,
                response.status,
            )
            return None
        except Exception as error:
            logging.error(
                "Unexpected error while deleting project ID %s: %s",
                project_id,
                error,
            )
            return None
