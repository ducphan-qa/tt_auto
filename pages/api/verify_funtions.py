import logging


class VerifyFunctions:
    def _get_response_text(self, response):
        try:
            return response.text()
        except Exception:
            return "<response body unavailable>"

    def _get_json(self, response_or_json):
        try:
            if isinstance(response_or_json, (dict, list)):
                return response_or_json

            if not hasattr(response_or_json, "json"):
                logging.error(
                    "Expected a Playwright response object or parsed JSON but got %s",
                    type(response_or_json).__name__,
                )
                return None

            return response_or_json.json()
        except Exception as error:
            response_text = self._get_response_text(response_or_json)
            logging.error(
                "Failed to parse response JSON: %s. Response body: %s",
                error,
                response_text,
            )
            return None

    def _assert_status(self, response, expected_status_code: int):
        try:
            actual_status_code = response.status
            response_text = self._get_response_text(response)

            if actual_status_code != expected_status_code:
                logging.error(
                    "Status code verification failed. Expected %s but got %s. "
                    "Response body: %s",
                    expected_status_code,
                    actual_status_code,
                    response_text,
                )
                return False

            logging.info(f"{expected_status_code}. Status code verification passed")
            return True
        except Exception as error:
            logging.error("Status code verification error: %s", error)
            return False

    def _assert_json_not_empty(self, response):
        try:
            response_json = self._get_json(response)

            if response_json in (None, {}, []):
                logging.error("Response JSON is empty")
                return None

            logging.info("JSON is not empty. JSON response verification passed")
            return response_json
        except Exception as error:
            logging.error("JSON response verification error: %s", error)
            return None

    def _assert_value_of_key_in_json(
        self,
        response_or_json,
        expected_values: dict,
    ):
        try:
            response_json = self._get_json(response_or_json)

            if not response_json:
                logging.error("Response JSON is empty")
                return False

            if not isinstance(response_json, dict):
                logging.error(
                    "Expected response JSON to be a dictionary but got %s",
                    type(response_json).__name__,
                )
                return False

            verification_passed = True

            for key, expected_value in expected_values.items():
                try:
                    if key not in response_json:
                        logging.error("Key '%s' not found in response JSON", key)
                        verification_passed = False
                        continue

                    actual_value = response_json[key]
                    if actual_value != expected_value:
                        logging.error(
                            "Expected '%s' to be '%s' but got '%s'",
                            key,
                            expected_value,
                            actual_value,
                        )
                        verification_passed = False
                        continue

                    logging.info("Key '%s' value verification passed", key)
                except Exception as error:
                    logging.error("Key '%s' verification error: %s", key, error)
                    verification_passed = False

            if verification_passed:
                logging.info("Expected key/value verification passed")

            return verification_passed
        except Exception as error:
            logging.error("Expected key/value verification error: %s", error)
            return False

    def assert_status(self, response, expected_status_code: int):
        return self._assert_status(response, expected_status_code)

    def assert_json_not_empty(self, response):
        return self._assert_json_not_empty(response)

    def assert_value_of_key_in_json(self, response_or_json, expected_values: dict):
        return self._assert_value_of_key_in_json(response_or_json, expected_values)
