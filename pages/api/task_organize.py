import logging
import dotenv, os
import time

from pages.api.verify_funtions import VerifyFunctions
from playwright.sync_api import APIRequestContext

dotenv.load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
BASE_PATH = "/open/v1"


class TaskOrganize:
    def __init__(self, api_request_context: APIRequestContext) -> None:
        self.request = api_request_context
        self.project_id_default = PROJECT_ID

        assert self.project_id_default, "PROJECT_ID is not set"
        self.verify_funtion = VerifyFunctions()

    def _expected_statuses(self, expected_status):
        if isinstance(expected_status, (list, tuple, set, range)):
            return tuple(expected_status)
        return (expected_status,)

    def _project_id(self, project_id=None):
        return project_id or self.project_id_default

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

    def get_task(self, task_id: str, expected_status=200, project_id=None):
        """Get Task By Project ID And Task ID"""
        project_id = self._project_id(project_id)
        try:
            logging.info(
                "Sending GET request to fetch task ID: %s from project ID: %s",
                task_id,
                project_id,
            )
            response = self._send_request(
                "get",
                f"{BASE_PATH}/project/{project_id}/task/{task_id}"
            )
            expected_statuses = self._expected_statuses(expected_status)

            if 404 in expected_statuses:
                if response.status == 404:
                    logging.info("Task ID %s returned 404 as expected", task_id)
                    return None

                if response.status in expected_statuses and response.status != 200:
                    logging.info(
                        "Task ID %s returned expected status %s from project ID %s",
                        task_id,
                        response.status,
                        project_id,
                    )
                    return response

                if response.status == 200:
                    response_text = self.verify_funtion._get_response_text(response)
                    if not response_text.strip():
                        logging.info(
                            "Task ID %s returned 200 with empty body while expected "
                            "404. Treating as not found.",
                            task_id,
                        )
                        return None

                    logging.info(
                        "Task ID %s is still retrievable after delete. "
                        "It may still be stored in Trash.",
                        task_id,
                    )
                    return response.json()

                logging.error(
                    "Cannot verify deleted task ID %s from project ID %s. "
                    "Expected status: %s. Actual status: %s. Response body: %s",
                    task_id,
                    project_id,
                    expected_statuses,
                    response.status,
                    self.verify_funtion._get_response_text(response),
                )
                return None

            if response.status not in expected_statuses:
                logging.error(
                    "Cannot fetch task ID %s from project ID %s. Expected status: "
                    "%s. Actual status: %s. Response body: %s",
                    task_id,
                    project_id,
                    expected_statuses,
                    response.status,
                    self.verify_funtion._get_response_text(response),
                )
                return None

            if response.status == 200:
                self.verify_funtion._assert_json_not_empty(response)
                response_json = response.json()
                logging.debug("Task ID is: %s", response_json.get("id"))
                logging.debug("Task title is: %s", response_json.get("title"))
                logging.debug("Task content is: %s", response_json.get("content"))
                logging.debug("Task project ID is: %s", response_json.get("projectId"))
                logging.debug("Task priority is: %s", response_json.get("priority"))
                return response_json

            logging.info(
                "Task ID %s returned expected status %s from project ID %s",
                task_id,
                response.status,
                project_id,
            )
            return response
        except Exception as error:
            logging.error("Unexpected error while fetching task ID %s: %s", task_id, error)
            return None

    def create_task(
        self,
        task_title: str = "Default New Task",
        task_content: str = "This is task default content",
        project_id=None,
        expected_status=200,
        extra_fields=None,
    ):
        project_id = self._project_id(project_id)
        try:
            body = {
                "title": task_title,
                "projectId": project_id,
                "content": task_content,
            }
            if extra_fields:
                body.update(extra_fields)

            logging.info(
                "Sending POST request to create task in project ID: %s",
                project_id,
            )
            logging.debug("Create task request body: %s", body)
            response = self._send_request("post", f"{BASE_PATH}/task", data=body)
            expected_statuses = self._expected_statuses(expected_status)

            if response.status not in expected_statuses:
                logging.error(
                    "Cannot create task in project ID %s. Expected status: %s. "
                    "Actual status: %s. Response body: %s",
                    project_id,
                    expected_statuses,
                    response.status,
                    self.verify_funtion._get_response_text(response),
                )
                return None

            if response.status == 200:
                self.verify_funtion._assert_json_not_empty(response)
                response_json = response.json()
                logging.debug("Created task ID is: %s", response_json.get("id"))
                logging.debug("Created task title is: %s", response_json.get("title"))
                logging.debug(
                    "Created task content is: %s", response_json.get("content")
                )
                logging.debug(
                    "Created task project ID is: %s", response_json.get("projectId")
                )
                logging.debug(
                    "Created task priority is: %s", response_json.get("priority")
                )
                return response_json

            logging.info(
                "Create task returned expected status %s for project ID %s",
                response.status,
                project_id,
            )
            return response
        except Exception as error:
            logging.error("Unexpected error while creating task: %s", error)
            return None

    def delete_task(self, task_id: str, expected_status=200, project_id=None):
        project_id = self._project_id(project_id)
        try:
            logging.info(
                "Sending DELETE request to delete task ID: %s from project ID: %s",
                task_id,
                project_id,
            )
            response = self._send_request(
                "delete",
                f"{BASE_PATH}/project/{project_id}/task/{task_id}"
            )
            expected_statuses = self._expected_statuses(expected_status)

            if response.status not in expected_statuses:
                logging.error(
                    "Cannot delete task ID %s from project ID %s. Expected status: "
                    "%s. Actual status: %s. Response body: %s",
                    task_id,
                    project_id,
                    expected_statuses,
                    response.status,
                    self.verify_funtion._get_response_text(response),
                )
                return None

            if response.status in expected_statuses:
                logging.info("Successfully deleted task ID: %s", task_id)
                return response

            return None
        except Exception as error:
            logging.error("Unexpected error while deleting task ID %s: %s", task_id, error)
            return None

    def update_task(self, task_id: str, content_dict: dict, expected_status=200):
        try:
            logging.info("Sending POST request to update task ID: %s", task_id)
            logging.debug("Update task request body: %s", content_dict)
            response = self._send_request(
                "post",
                f"{BASE_PATH}/task/{task_id}",
                data=content_dict,
            )
            expected_statuses = self._expected_statuses(expected_status)

            if response.status not in expected_statuses:
                logging.error(
                    "Cannot update task ID %s. Expected status: %s. Actual status: "
                    "%s. Response body: %s",
                    task_id,
                    expected_statuses,
                    response.status,
                    self.verify_funtion._get_response_text(response),
                )
                return None

            if response.status == 200:
                response_text = self.verify_funtion._get_response_text(response)
                if not response_text.strip():
                    logging.info(
                        "Update task ID %s returned 200 with empty response body",
                        task_id,
                    )
                    return response

                self.verify_funtion._assert_json_not_empty(response)
                response_json = response.json()
                logging.info("Successfully updated task ID: %s", task_id)
                logging.debug("Updated task ID is: %s", response_json.get("id"))
                logging.debug("Updated task title is: %s", response_json.get("title"))
                logging.debug("Updated task content is: %s", response_json.get("content"))
                logging.debug(
                    "Updated task project ID is: %s", response_json.get("projectId")
                )
                logging.debug(
                    "Updated task priority is: %s", response_json.get("priority")
                )
                return response_json

            logging.info(
                "Update task ID %s returned expected status %s",
                task_id,
                response.status,
            )
            return response
        except Exception as error:
            logging.error("Unexpected error while updating task ID %s: %s", task_id, error)
            return None

    def complete_task(self, project_id, task_id: str, expected_status=200):
        project_id = self._project_id(project_id)
        try:
            logging.info(
                "Sending POST request to complete task ID: %s using project ID: %s",
                task_id,
                project_id,
            )
            response = self._send_request(
                "post",
                f"{BASE_PATH}/project/{project_id}/task/{task_id}/complete"
            )
            expected_statuses = self._expected_statuses(expected_status)

            if response.status not in expected_statuses:
                logging.error(
                    "Cannot complete task ID %s using project ID %s. Expected "
                    "status: %s. Actual status: %s. Response body: %s",
                    task_id,
                    project_id,
                    expected_statuses,
                    response.status,
                    self.verify_funtion._get_response_text(response),
                )
                return None

            if response.status in expected_statuses:
                logging.info("Successfully completed task ID: %s", task_id)
                return response

            return None
        except Exception as error:
            logging.error(
                "Unexpected error while completing task ID %s: %s", task_id, error
            )
            return None

    def move_task(self, from_project_id, to_project_id, task_id, expected_status=200):
        try:
            body = [
                {
                    "fromProjectId": from_project_id,
                    "toProjectId": to_project_id,
                    "taskId": task_id,
                }
            ]

            logging.info(
                "Sending POST request to move task ID: %s from project ID: %s "
                "to project ID: %s",
                task_id,
                from_project_id,
                to_project_id,
            )
            logging.debug("Move task request body: %s", body)
            response = self._send_request("post", f"{BASE_PATH}/task/move", data=body)

            expected_statuses = (
                tuple(expected_status)
                if isinstance(expected_status, (list, tuple, set))
                else (expected_status,)
            )

            if response.status in expected_statuses:
                logging.info(
                    "Move task response status %s matched expected status for task "
                    "ID: %s from project ID: %s to project ID: %s",
                    response.status,
                    task_id,
                    from_project_id,
                    to_project_id,
                )
                return response

            logging.error(
                "Cannot move task ID %s from project ID %s to project ID %s. "
                "Expected status: %s. Actual status: %s. Response body: %s",
                task_id,
                from_project_id,
                to_project_id,
                expected_statuses,
                response.status,
                self.verify_funtion._get_response_text(response),
            )
            return None
        except Exception as error:
            logging.error("Unexpected error while moving task ID %s: %s", task_id, error)
            return None

    def batch_add_tasks(self, task_payloads):
        created_tasks = []
        try:
            for payload in task_payloads:
                created_task = self.create_task(
                    task_title=payload["title"],
                    task_content=payload.get("content", ""),
                    project_id=payload.get("projectId"),
                    extra_fields={
                        key: value
                        for key, value in payload.items()
                        if key not in {"title", "content", "projectId"}
                    },
                )
                if created_task is None:
                    return None
                created_tasks.append(created_task)
            return created_tasks
        except Exception as error:
            logging.error("Unexpected error while batch adding tasks: %s", error)
            return None

    def batch_update_tasks(self, task_payloads):
        updated_tasks = []
        try:
            for payload in task_payloads:
                task_id = payload["id"]
                updated_task = self.update_task(task_id, payload)
                if updated_task is None:
                    return None
                updated_tasks.append(updated_task)
            return updated_tasks
        except Exception as error:
            logging.error("Unexpected error while batch updating tasks: %s", error)
            return None

    def filter_tasks_by_project(self, project_id=None, status=None):
        project_id = self._project_id(project_id)
        try:
            response = self._send_request(
                "get",
                f"{BASE_PATH}/project/{project_id}/data",
            )
            if response.status != 200:
                logging.error(
                    "Cannot filter tasks for project ID %s. Status: %s. "
                    "Response body: %s",
                    project_id,
                    response.status,
                    self.verify_funtion._get_response_text(response),
                )
                return None

            project_data = response.json()
            tasks = project_data.get("tasks", [])
            if status is None:
                return tasks

            statuses = set(status if isinstance(status, (list, tuple, set)) else [status])
            return [item for item in tasks if item.get("status") in statuses]
        except Exception as error:
            logging.error(
                "Unexpected error while filtering tasks for project ID %s: %s",
                project_id,
                error,
            )
            return None

    def search_tasks_by_title(self, title_query, project_id=None):
        try:
            tasks = self.filter_tasks_by_project(project_id=project_id)
            if tasks is None:
                return None

            normalized_query = title_query.casefold()
            return [
                item
                for item in tasks
                if normalized_query in item.get("title", "").casefold()
            ]
        except Exception as error:
            logging.error("Unexpected error while searching tasks: %s", error)
            return None
