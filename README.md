# TickTick Automation Test Project

Automation test project for validating TickTick API and web behavior using **Python**, **pytest**, **Playwright**, and **uv**.

This project is designed for API, sanity, regression, and integration testing between **Project** and **Task** features.

---

## Tech Stack

- Python
- uv
- pytest
- pytest-playwright
- Playwright
- python-dotenv

---

## Project Setup

### 1. Initialize project with uv

```bash
uv init .
```

> Note: use `uv init .`, not `unit init .`.

### 2. Install dependencies

```bash
uv add pytest-playwright
uv add python-dotenv
```

### 3. Install Playwright browsers

```bash
uv run playwright install
```

### 4. Run tests

```bash
uv run pytest
```

---

## Test Markers

This project uses pytest markers to control test execution by scope and purpose.

Supported markers:

| Marker | Purpose |
|---|---|
| `api` | API test cases |
| `sanity` | Core sanity test cases |
| `regression` | Regression and integration test cases |

---

## Run Tests by Marker

### Run all API tests

```bash
uv run pytest -m api
```

### Run regression tests only

```bash
uv run pytest -m regression
```

### Run tests marked as both API and regression

```bash
uv run pytest -m "api and regression"
```

### Exclude regression tests

```bash
uv run pytest -m "not regression"
```

---

## Recommended `pytest.ini`

Create a `pytest.ini` file in the project root to register markers and avoid unknown marker warnings.

```ini
[pytest]
markers =
    api: API test cases
    sanity: Basic validation test cases for core features
    regression: Regression test cases and integration flows
```

---

## Test File Naming Rules

All test files should follow this format:

```text
test_[function_code]_[scope_code]_[test_case_number].py
```

Example:

```text
test_CT_TC01.py
```

Recommended format:

```text
test_[function_need_to_verify]_[task_or_project_or_integrate]_[test_case_number].py
```

---

## Function Codes

### Task Function Codes

| Code | Meaning |
|---|---|
| `C` | Create Task |
| `G` | Get Task |
| `D` | Delete Task |
| `U` | Update Task |
| `M` | Move Task |
| `F` | Filter Task |

### Project Function Codes

| Code | Meaning |
|---|---|
| `C` | Create Project |
| `GU` | Get User Project |
| `GID` | Get Project by ID |
| `D` | Delete Project |
| `U` | Update Project |

---

## Scope Codes

| Code | Meaning | Test Type |
|---|---|---|
| `T` | Task only | Sanity |
| `P` | Project only | Sanity |
| `IPT` | Integration between Project and Task | Regression |

---

## Naming Examples

### Task test cases

```text
test_CT_TC01.py     # Create Task - Sanity
test_GT_TC02.py     # Get Task - Sanity
test_UT_TC03.py     # Update Task - Sanity
test_DT_TC04.py     # Delete Task - Sanity
test_MT_TC05.py     # Move Task - Sanity
test_FT_TC06.py     # Filter Task - Sanity
```

### Project test cases

```text
test_CP_TC01.py       # Create Project - Sanity
test_GUP_TC02.py      # Get User Project - Sanity
test_GIDP_TC03.py     # Get Project by ID - Sanity
test_UP_TC04.py       # Update Project - Sanity
test_DP_TC05.py       # Delete Project - Sanity
```

### Integration test cases

```text
test_CIPT_TC01.py     # Create Project and Task - Regression
test_GIPT_TC02.py     # Get Project with Task - Regression
test_DIPT_TC03.py     # Delete Project with Task - Regression
```

---

## TickTick Web Areas

Main UI areas covered by web automation:

```text
sidebar
project-list-scroller
task-list-view
detail-view
```

---

## Suggested Page Object Mapping

```text
pages/
├── sidebar_page.py
├── project_list_page.py
├── task_list_page.py
└── detail_view_page.py
```

| Page Object | Responsibility |
|---|---|
| `sidebar_page.py` | Navigation, project shortcuts, main menu actions |
| `project_list_page.py` | Project list, project selection, project visibility |
| `task_list_page.py` | Task list, task selection, task state |
| `detail_view_page.py` | Task detail, title, description, due date, priority, comments |

---

## Suggested Project Structure

```text
.
├── pages/
│   ├── sidebar_page.py
│   ├── project_list_page.py
│   ├── task_list_page.py
│   └── detail_view_page.py
│
├── tests/
│   ├── api/
│   │   ├── task/
│   │   └── project/
│   │
│   ├── web/
│   │   ├── task/
│   │   └── project/
│   │
│   └── integration/
│
├── utils/
│   ├── config.py
│   ├── api_client.py
│   └── test_data.py
│
├── .env
├── pytest.ini
├── pyproject.toml
└── README.md
```

---

## Environment Variables

Create a `.env` file in the project root for local test runs. Do not upload this
file to GitHub and do not commit it to source control.

```env
TICKTICK_API_URL=https://api.ticktick.com/api/v2
API_KEY=replace_with_ticktick_api_key
PROJECT_ID=replace_with_ticktick_project_id
TICKTICK_USERNAME=replace_with_ticktick_username
TICKTICK_PASSWORD=replace_with_ticktick_password
TICKTICK_STATE_PATH=pages/web/state.json
```

`TICKTICK_STATE_PATH` is optional for local runs. If it is not set, the project
uses `pages/web/state.json`.

### GitHub Actions CI Secrets

For CI, add these repository secrets in GitHub:

1. Open your GitHub repository.
2. Go to `Settings` -> `Secrets and variables` -> `Actions`.
3. Select `New repository secret`.
4. Add each secret below exactly by name.

| Secret name | Value |
|---|---|
| `TICKTICK_API_URL` | TickTick API base URL, for example `https://api.ticktick.com/api/v2` |
| `API_KEY` | TickTick API bearer token |
| `PROJECT_ID` | Project/list ID used by API tests |
| `TICKTICK_USER` | TickTick login username or email for CI |
| `TICKTICK_PASS` | TickTick login password for CI |

Do not create a GitHub secret for `TICKTICK_STATE_PATH`. The workflow creates it
automatically from `$RUNNER_TEMP` so the Playwright login state stays outside the
repository workspace.

The CI workflow maps `TICKTICK_USER` and `TICKTICK_PASS` into the runtime
environment variables `TICKTICK_USERNAME` and `TICKTICK_PASSWORD`.

Recommended `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
.pytest_cache/
test-results/
playwright-report/
```

---

## Example Test Marker Usage

```python
import pytest


@pytest.mark.api
@pytest.mark.sanity
def test_create_task_successfully():
    assert True
```

```python
import pytest


@pytest.mark.api
@pytest.mark.regression
def test_create_project_then_create_task_successfully():
    assert True
```

---

## Recommended Test Strategy

### Sanity

Use sanity tests for core standalone flows:

```text
Create Task
Get Task
Update Task
Delete Task
Create Project
Get Project
Update Project
Delete Project
```

### Regression

Use regression tests for integration or cross-feature behavior:

```text
Create Project -> Create Task under Project
Move Task between Projects
Delete Project -> Verify related Task behavior
Filter Task by Project
Verify Task detail after Project update
```

### API

Use API tests for direct backend validation:

```text
Status code
Response schema
Required fields
Error handling
Data persistence
Authorization behavior
```

### Web

Use web tests for user-facing validation:

```text
Sidebar navigation
Project list rendering
Task list rendering
Task detail view behavior
Create/update/delete from UI
```

---

## Common Commands

### Run all tests

```bash
uv run pytest
```

### Run with verbose output

```bash
uv run pytest -v
```

### Run a specific file

```bash
uv run pytest tests/api/task/test_CT_TC01.py
```

### Run a specific test function

```bash
uv run pytest tests/api/task/test_CT_TC01.py::test_create_task_successfully
```

### Run headed Playwright tests

```bash
uv run pytest --headed
```

### Run with browser selection

```bash
uv run pytest --browser chromium
```

---

## Contribution Rules

Before adding a new test case:

1. Follow the test naming convention.
2. Add the correct pytest markers.
3. Keep API tests independent.
4. Keep web selectors inside Page Object files.
5. Do not hardcode credentials or tokens.
6. Use shared utilities for test data and API requests.
7. Clean up created test data when possible.

---

## Quality Checklist

Before pushing code:

```bash
uv run pytest -m "sanity"
uv run pytest -m "api"
uv run pytest -m "not regression"
```

For full validation:

```bash
uv run pytest
```

---

## Notes

- Use `sanity` for quick validation of core Task and Project features.
- Use `regression` for integration flows between Project and Task.
- Use `api` for backend/API-level validation.
- Use Page Object Model for TickTick web automation.
- Keep test data isolated to avoid flaky tests.
