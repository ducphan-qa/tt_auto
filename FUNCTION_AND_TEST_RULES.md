# Global Function And Test File Rules

## Purpose

Use this guide as a global standard for writing functions and test files in any software project. The rules are technology-neutral and can be applied to backend, frontend, automation, library, command-line, data, or service projects.

The goal is to keep code easy to read, easy to test, and easy to reuse across projects.

## Project Structure Rules

- Group source code by responsibility, not by random implementation detail.
- Keep reusable product logic separate from test code.
- Keep shared test helpers in a clear helper module or test utility folder.
- Keep configuration, fixtures, constants, and generated reports separate from feature code.
- Prefer this general shape when possible:

```text
project/
  src/ or app/
    feature_or_module/
      main_logic.py
      validators.py
      helpers.py
  tests/
    feature_or_module/
      test_feature_scenario.py
    helpers.py
  config/
  reports/
  README.md
```

- Do not place large business workflows directly inside test files when they can be reused.
- Do not mix generated output, reports, screenshots, caches, or logs with source modules.

## Function Naming Rules

- Use clear verb-based names that describe the action.
- Prefer names that follow this shape:

```text
<action>_<resource>()
<action>_<resource>_<condition>()
<action>_<resource>_if_<condition>()
```

- Use common action prefixes consistently:

| Prefix | Use For |
|---|---|
| `create_*` | Creating a new resource, object, record, file, session, or state |
| `get_*` | Reading or retrieving one resource |
| `list_*` | Reading multiple resources |
| `find_*` | Searching for a resource that may or may not exist |
| `update_*` | Changing an existing resource |
| `delete_*` | Removing an existing resource |
| `move_*` | Moving ownership, location, category, or state |
| `build_*` | Constructing a payload, object, request, command, or data structure |
| `parse_*` | Converting raw input into structured data |
| `format_*` | Converting data into display or output format |
| `validate_*` | Checking whether data is valid and returning a result |
| `verify_*` | Checking observable behavior or state |
| `assert_*` | Failing immediately when an expected condition is not met |
| `cleanup_*` | Removing temporary data or restoring state |
| `*_if_exists` | Performing a cleanup or action safely when the target may be missing |

- Use private helper names with a leading underscore only when the function is internal to the module or class.
- Avoid vague names such as `handle_data`, `process_stuff`, `do_test`, `run_all`, or `check_result`.
- Do not hide important behavior behind names that are too short or too generic.

## Function Design Rules

- Each function should have one main responsibility.
- Function inputs should be explicit parameters, not hidden global state, unless the value is true configuration.
- Return useful values from action functions when later code needs IDs, status, created objects, or computed output.
- Use type hints where they make the contract easier to understand.
- Keep functions small enough that their setup, action, and result are easy to scan.
- Prefer early returns for invalid or unsupported states when that makes the function clearer.
- Do not silently ignore unexpected errors. Either raise the error, return a clear failure result, or log enough context to debug.
- Keep logging meaningful:
  - Log high-level actions at info level.
  - Log diagnostic details at debug level.
  - Log failed expectations or recoverable failures at warning or error level.
- Do not log secrets, tokens, passwords, private keys, or sensitive personal data.
- Avoid mixing validation, mutation, and cleanup in one function unless the function is explicitly a workflow helper.

## Helper And Utility Function Rules

- Use helpers when the same setup, data creation, assertion, or cleanup appears in multiple places.
- Helper names should explain the intent, not the implementation.
- Good helper examples:

```python
def unique_text(prefix: str) -> str:
    ...

def create_temp_resource(client, prefix: str):
    ...

def cleanup_resource_if_exists(client, resource_id: str | None) -> None:
    ...
```

- Helpers should accept the data they need instead of reaching into unrelated modules.
- Helpers that create temporary data should return the identifiers needed for cleanup.
- Cleanup helpers should be safe to call when the resource was never created.
- Avoid over-general helpers that need many flags to behave correctly.

## Validation And Assertion Rules

- Use `validate_*` when the function checks data and returns a boolean, result object, or error list.
- Use `assert_*` when failure should immediately stop the current test or workflow.
- Use `verify_*` when checking externally visible behavior or state.
- Assertion messages should explain what failed and include useful context.
- Prefer specific assertions over broad truthy checks.

```python
assert created_resource is not None, "Create resource returned empty result"
assert "id" in created_resource, f"Resource id missing: {created_resource}"
assert actual_status == expected_status
```

- Validate both the operation result and the important fields affected by the operation.
- For negative cases, assert the expected failure behavior, not only that "something failed".

## Test File Naming Rules

- Test files must be easy to discover and easy to connect to a feature or scenario.
- Use a consistent test file prefix, usually `test_`.
- Prefer one of these generic formats:

```text
test_<feature>_<scenario>.py
test_<action>_<resource>_<condition>.py
test_<feature>_<number>.py
test_<workflow>_<expected_result>.py
```

- Examples:

```text
test_user_login_success.py
test_create_invoice_with_required_fields.py
test_update_profile_invalid_email.py
test_file_import_large_csv.py
test_checkout_payment_declined.py
```

- Group test files by feature, module, or workflow:

```text
tests/
  user/
    test_create_user_valid_data.py
    test_update_user_invalid_email.py
  billing/
    test_create_invoice_with_tax.py
    test_payment_declined.py
  integration/
    test_user_subscription_workflow.py
```

- Avoid file names that only contain ticket IDs unless the scenario is also clear.
- If numeric case IDs are required, put them after a readable feature or scenario name.

```text
test_create_invoice_TC01.py
test_REG_user_subscription_001.py
```

## Test Function Naming Rules

- Test function names should describe expected behavior.
- Prefer one of these formats:

```text
test_<action>_<resource>_<condition>()
test_should_<expected_behavior>_when_<condition>()
test_<workflow>_<expected_result>()
test_reject_<action>_when_<invalid_condition>()
```

- Examples:

```python
def test_create_user_with_valid_email():
    ...

def test_should_return_empty_result_when_no_records_match():
    ...

def test_reject_payment_when_card_is_expired():
    ...

def test_import_workflow_preserves_existing_records():
    ...
```

- Avoid names such as `test_case_1`, `test_happy_path`, or `test_bug`.
- If a test covers a known defect or requirement, include the behavior in the name and put the ticket ID in a comment, marker, or metadata.

## Test Structure Rules

- Each test should have a clear flow:

```text
Arrange / Setup
Act / Execute
Assert / Verify
Cleanup / Restore
```

- Keep tests independent. One test should not require another test to run first.
- Tests should create or prepare the data they need.
- Tests should clean up temporary data when possible.
- Use `try/finally` or fixture cleanup when a test creates external state.
- Keep assertions close to the behavior being verified.
- Do not hide the main purpose of the test behind too many helper calls.
- Use reusable helpers for noisy setup and cleanup, but keep the important action and expected result visible in the test.
- Avoid sleeps or fixed waits unless there is no reliable event, state, or polling mechanism available.
- For workflows, verify important state after each major transition.

## Test Data And Cleanup Rules

- Test data should be unique when tests create shared or persistent resources.
- Use readable prefixes that identify the test or workflow.
- Do not hardcode secrets or environment-specific credentials in tests.
- Put environment-specific values in configuration or environment variables.
- Temporary resources should be cleaned up even if the test fails.
- Cleanup functions should tolerate already-deleted or missing resources.
- Use constants for expected statuses, fixed options, or shared scenario values.
- Keep mutation-heavy tests isolated from read-only tests.

Example cleanup pattern:

```python
resource_id = None

try:
    resource = create_temp_resource(client, "scenario-name")
    resource_id = resource["id"]

    result = update_resource(client, resource_id, {"name": "Updated"})

    assert result["name"] == "Updated"
finally:
    cleanup_resource_if_exists(client, resource_id)
```

## Markers Or Tags Rules

- Use markers, tags, labels, or metadata to describe test purpose and execution scope.
- Keep marker names stable and documented.
- Common marker categories:

| Marker | Use For |
|---|---|
| `unit` | Small isolated code behavior |
| `integration` | Multiple modules or services working together |
| `e2e` | Full user or system workflow |
| `smoke` | Minimal critical checks |
| `sanity` | Core feature validation after change |
| `regression` | Existing behavior that must not break |
| `slow` | Tests that are expensive or long-running |
| `negative` | Invalid input or failure behavior |

- A test may have more than one marker when it belongs to multiple useful groups.
- Mark known product defects or unsupported behavior as expected failures only when the reason is documented.
- Do not use expected-failure markers to hide flaky or poorly written tests.

## Global Checklist For New Projects

Use this checklist before adding or reviewing new functions and test files.

- Function names use clear action prefixes.
- Each function has one main responsibility.
- Inputs, outputs, and failure behavior are clear.
- Shared setup, validation, and cleanup are moved into reusable helpers.
- Assertions are specific and include useful failure messages.
- Test files follow a consistent naming format.
- Test function names describe behavior and conditions.
- Tests are independent and can run in any order.
- Tests use setup, action, assertion, and cleanup structure.
- Temporary data is unique and cleaned up safely.
- Secrets and environment-specific values are not hardcoded.
- Markers or tags are registered, documented, and meaningful.
- Known failures include a clear reason.
- Generated reports, logs, screenshots, and caches are kept out of source modules.
