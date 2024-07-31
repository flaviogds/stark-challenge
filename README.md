# STARKBANK - INVOICE

## Description
The application is part of the skill test for the StarkBank backend team and consists of an API that receives requests to create invoices, makes the request via SDK/API for StarkBank and after receiving payment confirmation, the amount is transferred to a new account still at StarkBank.

## Requirements

- Python 3.11 or higher stable version
- Poetry `(recommend)`

    > Note: This project is based on pyproject.toml, use a package manager such as compatible with PEP 518 for dependency management.

## How to Run the Application
To run the application locally, follow the steps below:
1. Clone the repository
2. Access the project directory: `cd stark-challenge`
3. Install dependencies: 

```bash
$ poetry installation
```

4. Configure environment variables:

```
ORGANIZATION_ID = "your_organization_id"
PROJECT_ID = "your_project_id"
MODE = "ambience"
TRANSFER_ACCOUNT = { "bank_code": "your_bank_code", "branch_code": "your_branch_code", "account_number": "your_account_number", "name": "your_account_name", "tax_id": "your_tax_id", "account_type": "payment" }
SSL_KEY = "your_private_key_on_base64"
GOOGLE_CREDENTIALS = "gooogle_credentials_on_json"
```

5. Launch the application:
```
fastapi dev --host 0.0.0.0 --port=80 --reload ./src/main.py 
```

## How to Run the Tests
The application has a `Makefile` and a set of commands to facilitate access.

### Commands Reference

| Command           | Description                                                    |
| ----------------- | -------------------------------------------------------------- |
| `run` <param>     | Run the application.                                           |
| `test`            | Run code quality tests with coverage.                          |
| `test-coverage`   | Generate a coverage report.                                    |
| `coverage-browser`| Generate an HTML coverage report and open it in a web browser. |
| `lint`            | Perform linting using pylint.                                  |
| `format`          | Format the source code using `pyink` and `isort`.              |
| `security-checks` | Perform security checks using `bandit`.                        |

    More commands are disponibles to use with docker and docker-compose

## How to deploy

The application has a ready-to-use Dockerfile, which makes it possible to deploy to any cloud or infrastructure provider.
To deploy this application, we chose to implement it in Google CloudRun, a self-managed serverless environment.
A YAML file prepared for deployment on GCP using Google Cloud Build and the respective configuration compatible with OpenApi2 for deploying an API Gateway.