# GitHub Gist API

A lightweight REST API built using **Python and FastAPI** to retrieve publicly available GitHub Gists for a given GitHub username. The application integrates with the GitHub REST API, provides basic error handling and logging, includes automated tests, and supports Docker containerization.

## 1. Project Overview

The application exposes an HTTP GET endpoint that accepts a GitHub username and retrieves the user's publicly available Gists.

For example:

```http
GET /octocat
```

The application communicates with the GitHub REST API:

```text
https://api.github.com/users/{username}/gists
```

The GitHub API response is returned to the API consumer as JSON.

### Key Features

- Retrieve publicly available GitHub Gists using a username.
- Asynchronous HTTP requests using HTTPX.
- Configuration management using environment variables.
- Configurable HTTP request timeout.
- Centralized application logging.
- Error handling for upstream API failures.
- Automated API tests using Pytest and FastAPI TestClient.
- Mock external API responses using HTTPX MockTransport.
- Dockerfile for containerized execution.
- Application listens on port `8080`.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Application development |
| FastAPI | REST API framework |
| Uvicorn | ASGI application server |
| HTTPX | Asynchronous HTTP client |
| Pydantic Settings | Configuration management |
| Pytest | Automated testing |
| Docker | Application containerization |
| GitHub REST API | External Gist data source |

## 3. Project Structure

```text
github-gist-api/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── github_client.py
│   ├── routes.py
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── requirements.txt
└── README.md
```

### Application Modules

| File | Responsibility |
|---|---|
| `main.py` | Initializes the FastAPI application, configures logging and registers API routes. |
| `config.py` | Manages application configuration and environment variables. |
| `github_client.py` | Handles communication with the GitHub REST API using HTTPX. |
| `routes.py` | Defines API endpoints and maps upstream errors to HTTP responses. |
| `test_api.py` | Contains automated tests for API functionality and error handling. |

## 4. Application Architecture

The application follows a simple modular structure, separating API routing, external API communication and application configuration.

### Request Flow

```text
             API Consumer
                   |
                   |
             HTTP GET Request
                   |
                   v
             FastAPI Routes
                routes.py
                   |
                   |
             GitHub API Client
             github_client.py
                   |
                   |
             HTTPX AsyncClient
                   |
                   v
             GitHub REST API
                   |
                   |
             JSON Response
                   |
                   v
             FastAPI Routes
                   |
                   |
             HTTP Response
                   |
                   v
             API Consumer
```

### Application Responsibilities

1. FastAPI receives the incoming HTTP request.
2. The route extracts the GitHub username from the URL.
3. The GitHub client constructs the external API URL.
4. HTTPX sends an asynchronous GET request to GitHub.
5. The response status is checked and the JSON payload is parsed.
6. The retrieved Gist data is returned to the API consumer.
7. Upstream errors are translated into appropriate HTTP responses.

## 5. API Endpoints

### Root Endpoint

Returns a welcome message and basic API usage information.

**Request**

```http
GET /
```

**Response — HTTP 200**

```json
{
  "message": "Welcome to GitHub Gist API",
  "usage": "Use /{username} to retrieve public GitHub Gists",
  "example": "/octocat"
}
```

### Health Check Endpoint

Provides a basic application health response.

**Request**

```http
GET /health
```

**Response — HTTP 200**

```json
{
  "status": "healthy"
}
```

### Retrieve GitHub Gists

Retrieves publicly available Gists for the specified GitHub username.

**Request**

```http
GET /{username}
```

**Example**

```http
GET /octocat
```

**Response — HTTP 200**

Returns a JSON array containing the publicly available Gists retrieved from GitHub.

The response includes fields such as:

- Gist ID
- Description
- Public visibility
- Gist URL
- File details
- Creation and update timestamps
- Owner information

The application returns the upstream GitHub JSON response without transforming its schema.

## 6. Error Handling

The application handles common failures encountered while communicating with the GitHub REST API.

| Scenario | HTTP Status | Description |
|---|---:|---|
| Successful request | 200 | Gists retrieved successfully. |
| GitHub user not found | 404 | GitHub API indicates that the requested user does not exist. |
| GitHub API timeout | 504 | The upstream request exceeded the configured timeout. |
| Other GitHub HTTP errors | 502 | GitHub returned an unsuccessful HTTP response. |
| Network or communication failure | 502 | Unable to communicate with GitHub. |

**Note:** An existing GitHub user with no public Gists receives HTTP 200 with an empty JSON array (`[]`). This is a successful request, not an error.

## 7. Configuration

Application configuration is externalized using environment variables and Pydantic Settings.

The application supports the following configuration values:

| Variable | Default | Description |
|---|---|---|
| `GITHUB_API_BASE_URL` | `https://api.github.com` | GitHub REST API base URL. |
| `REQUEST_TIMEOUT` | `5.0` | Maximum duration for an HTTP request, in seconds. |
| `LOG_LEVEL` | `INFO` | Application logging level. |

### Local Configuration

Create a `.env` file in the project root:

```env
GITHUB_API_BASE_URL=https://api.github.com
REQUEST_TIMEOUT=5.0
LOG_LEVEL=INFO
```

The `.env.example` file provides a sample configuration.

The actual `.env` file is excluded from version control to avoid committing local configuration or sensitive values.

## 8. Local Setup and Execution

### Prerequisites

- Python 3.13 or compatible version.
- pip package manager.
- Internet connectivity to access the GitHub REST API.

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd github-gist-api
```

### Step 2: Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file using the values provided in `.env.example`.

### Step 5: Start the Application

```bash
uvicorn app.main:app --reload --port 8080
```

The application will be available at:

```text
http://127.0.0.1:8080
```

### Step 6: Test the API

Open the following URLs in a browser or use curl:

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/octocat
```

FastAPI also provides interactive API documentation at:

```text
http://localhost:8080/docs
```

## 9. Automated Testing

The application includes automated tests implemented using Pytest and FastAPI TestClient.

HTTPX MockTransport is used to simulate external GitHub API responses, allowing tests to run without depending on live GitHub API calls.

### Test Scenarios

| Test Case | Expected Result |
|---|---|
| Root endpoint | HTTP 200 and welcome message |
| Health endpoint | HTTP 200 and healthy status |
| Retrieve `octocat` Gists | HTTP 200 and meaningful Gist response |
| Unknown GitHub user | HTTP 404 |
| GitHub API timeout | HTTP 504 |

### Execute Tests

Run the following command from the project root:

```bash
pytest -v
```

The tests validate both successful API responses and selected failure scenarios.

## 10. Docker Containerization

The application includes a Dockerfile to build and run the API inside a container.

### Prerequisites

- Docker Engine or Docker Desktop.

### Step 1: Build the Docker Image

Run the following command from the project root:

```bash
docker build -t github-gist-api:v1 .
```

### Step 2: Verify the Image

```bash
docker images
```

### Step 3: Run the Container

```bash
docker run -d \
  --name github-gist-api-container \
  -p 8080:8080 \
  github-gist-api:v1
```

### Step 4: Verify Container Status

```bash
docker ps
```

### Step 5: Inspect Application Logs

```bash
docker logs github-gist-api-container
```

### Step 6: Test the Containerized Application

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/octocat
```

### Container Lifecycle Commands

Stop the container:

```bash
docker stop github-gist-api-container
```

Start an existing container:

```bash
docker start github-gist-api-container
```

Restart the container:

```bash
docker restart github-gist-api-container
```

Remove a stopped container:

```bash
docker rm github-gist-api-container
```

Remove the Docker image:

```bash
docker rmi github-gist-api:v1
```

## 11. Logging and Observability

The application uses Python's built-in logging module.

Logging is configured centrally during application initialization.

The application records useful events, including:

- Root endpoint access.
- GitHub API request initiation.
- Successful Gist retrieval and result count.
- GitHub API HTTP errors.
- Request timeouts.
- Network communication failures.

The logging level can be adjusted using the `LOG_LEVEL` environment variable.

## 12. Possible Future Improvements

The current implementation focuses on the assignment's core requirements. The following enhancements could be considered in a future iteration:

- Optional GitHub authentication token support to improve API rate-limit capacity.
- Pagination support for retrieving larger Gist collections.
- Response models to validate and standardize the API response schema.
- More comprehensive input validation.
- Structured logging and correlation IDs.
- Additional automated tests for other upstream failure scenarios.
- Health checks that verify external dependency availability.
- CI/CD integration for automated testing and Docker image builds.

These are potential improvements and are not implemented in the current version.

## 13. Scope and Design Considerations

The implementation intentionally keeps the architecture simple and modular.

The application separates API routing, external service integration, configuration and testing responsibilities without introducing unnecessary frameworks or infrastructure dependencies.

The Docker image is built locally and the container listens on port `8080`. Publishing the image to a container registry or deploying it to a cloud platform is outside the current project scope.

---

## License

This project was developed as part of a technical take-home exercise.
