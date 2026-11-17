# IS601 Module 11 - Calculation Model and Testing

This repository contains my Module 11 assignment for IS601. I extended the provided calculator project with a SQLAlchemy calculation model, Pydantic validation, additional tests, and a CI/CD pipeline.

## Features

- Supports addition, subtraction, multiplication, and division.
- Uses a SQLAlchemy `Calculation` model with `id`, `a`, `b`, `type`, `inputs`, `result`, and a `user_id` foreign key.
- Uses a factory method to create the correct calculation subclass.
- Uses Pydantic `CalculationCreate` and `CalculationRead` schemas to validate input and output.
- Rejects invalid calculation types, missing operands, and division by zero.
- Includes unit, integration, PostgreSQL database, and end-to-end tests.
- Uses GitHub Actions for testing, Trivy security scanning, and Docker Hub deployment.

**Note:** The project keeps the calculator webpage and existing routes from the starter project. The Module 11 work focuses on the calculation model and validation; it does not add new database-backed calculation routes.

## Technologies

Python 3.10, FastAPI, SQLAlchemy, Pydantic, PostgreSQL 17, pytest, Playwright, Docker, GitHub Actions, and Trivy.

## Setup (Ubuntu / WSL)

Clone the repository:

```bash
git clone https://github.com/Xiaodu7/Assignment11.git
cd Assignment11
```

Create a virtual environment and install dependencies:

```bash
python3.10 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Running the Application

Start the existing calculator application locally:

```bash
python main.py
```

Open `http://localhost:8000` in a browser. Stop the server with `Ctrl+C`.

Alternatively, build and run the Docker image:

```bash
docker build -t assignment11:local .
docker run --rm -p 127.0.0.1:8001:8000 assignment11:local
```

Open `http://localhost:8001` in a browser.

## Running Tests

The PostgreSQL integration tests require a **dedicated test database**. The test fixture creates and drops tables, so do not point `TEST_DATABASE_URL` at a database containing important data.

Start PostgreSQL 17 in Docker (local testing only):

```bash
docker run -d --name assignment11-test-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=assignment11_test \
  -p 127.0.0.1:5433:5432 postgres:17
```

Run unit and integration tests:

```bash
TEST_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5433/assignment11_test \
  python -m pytest tests/unit/ tests/integration/ -v
```

Install the Playwright browser and run end-to-end tests:

```bash
python -m playwright install chromium
python -m pytest tests/e2e/ -v
```

End-to-end tests start the app on port `8000`, so keep that port available. The `pytest.ini` file produces terminal and HTML coverage reports (`htmlcov/`).

**Verified local results:** 78 unit/integration tests passed, 3 E2E tests passed, and 93% coverage for the unit/integration run.

## CI/CD and Docker Hub

The GitHub Actions workflow runs three jobs in sequence:

1. **Test:** Runs unit, integration, and E2E tests with PostgreSQL.
2. **Security:** Builds the Docker image and scans for HIGH/CRITICAL findings with Trivy.
3. **Deploy:** Pushes the image to Docker Hub if the earlier jobs pass on `main`.

- [GitHub repository](https://github.com/Xiaodu7/Assignment11)
- [GitHub Actions](https://github.com/Xiaodu7/Assignment11/actions)
- [Docker Hub repository](https://hub.docker.com/r/xdu7/assignment11)

Pull the published image:

```bash
docker pull xdu7/assignment11:latest
```

## Project Structure

```text
app/models/calculation.py                 SQLAlchemy model and calculation factory
app/schemas/calculation.py                Pydantic schemas and validation
tests/unit/                               Unit tests
tests/integration/                        Schema, calculation, and PostgreSQL tests
tests/e2e/                                Browser-based tests
.github/workflows/test.yml                CI/CD workflow
Dockerfile                                Application container
requirements.txt                          Python dependencies
main.py                                   Existing calculator application
```

## Acknowledgment

This assignment builds on the instructor's [Module 11 starter repository](https://github.com/kaw393939/module11_is601). My changes include the `a` and `b` model fields, expanded validation and reading schemas, additional tests, dependency/security fixes, and CI/CD configuration for my own Docker Hub repository.
