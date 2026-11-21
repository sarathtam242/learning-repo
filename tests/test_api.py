import httpx
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import github_client, routes


# Create a test client for our FastAPI application.
client = TestClient(app)


# Sample Gist response used to simulate GitHub API data.
MOCK_GISTS = [
    {
        "id": "12345",
        "description": "Test Gist",
        "public": True,
        "html_url": "https://gist.github.com/octocat/12345"
    },
    {
        "id": "67890",
        "description": "Another Test Gist",
        "public": True,
        "html_url": "https://gist.github.com/octocat/67890"
    }
]


def create_mock_transport(status_code=200, response_data=None):
    """
    Create a mock transport to simulate GitHub API responses
    without making actual network requests.
    """

    def mock_github_response(request):
        return httpx.Response(
            status_code=status_code,
            json=response_data if response_data is not None else [],
            request=request
        )

    return httpx.MockTransport(mock_github_response)


# ---------------------------------------------------------
# Test 1: Verify the root endpoint.
# ---------------------------------------------------------

def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to GitHub Gist API"


# ---------------------------------------------------------
# Test 2: Verify the application health endpoint.
# ---------------------------------------------------------

def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# ---------------------------------------------------------
# Test 3: Verify the assignment's required octocat scenario.
# ---------------------------------------------------------

def test_get_octocat_gists():

    transport = create_mock_transport(
        status_code=200,
        response_data=MOCK_GISTS
    )

    # Keep the original function but supply our mock HTTP transport.
    original_function = github_client.fetch_user_gists

    async def mocked_fetch_user_gists(username):
        return await original_function(username, transport=transport)

    # Patch the function where routes.py actually uses it.
    with pytest.MonkeyPatch.context() as monkeypatch:

        monkeypatch.setattr(
            routes,
            "fetch_user_gists",
            mocked_fetch_user_gists
        )

        response = client.get("/octocat")

    # Verify the response status and actual Gist data.
    assert response.status_code == 200

    gists = response.json()

    assert isinstance(gists, list)
    assert len(gists) == 2
    assert gists[0]["id"] == "12345"
    assert gists[0]["public"] is True
    assert gists[1]["id"] == "67890"


# ---------------------------------------------------------
# Test 4: Verify handling when GitHub cannot find a user.
# ---------------------------------------------------------

def test_github_user_not_found():

    transport = create_mock_transport(
        status_code=404,
        response_data={"message": "Not Found"}
    )

    original_function = github_client.fetch_user_gists

    async def mocked_fetch_user_gists(username):
        return await original_function(username, transport=transport)

    with pytest.MonkeyPatch.context() as monkeypatch:

        monkeypatch.setattr(
            routes,
            "fetch_user_gists",
            mocked_fetch_user_gists
        )

        response = client.get("/unknown-user")

    assert response.status_code == 404
    assert response.json()["detail"] == "GitHub user not found"


# ---------------------------------------------------------
# Test 5: Verify handling when GitHub API request times out.
# ---------------------------------------------------------

def test_github_request_timeout():

    # Simulate a timeout instead of waiting for a real network timeout.
    def timeout_handler(request):
        raise httpx.ReadTimeout(
            "GitHub API request timed out",
            request=request
        )

    transport = httpx.MockTransport(timeout_handler)

    original_function = github_client.fetch_user_gists

    async def mocked_fetch_user_gists(username):
        return await original_function(username, transport=transport)

    with pytest.MonkeyPatch.context() as monkeypatch:

        monkeypatch.setattr(
            routes,
            "fetch_user_gists",
            mocked_fetch_user_gists
        )

        response = client.get("/octocat")

    assert response.status_code == 504
    assert response.json()["detail"] == "GitHub API request timed out"
