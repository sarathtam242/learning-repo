import httpx
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import github_client, routes

client = TestClient(app)

# Sample Gist data used to simulate GitHub API responses.
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


# Create a mock HTTP transport so tests do not make real GitHub API calls.
def create_mock_transport(status_code=200, response_data=None):
    def mock_github_response(request):
        return httpx.Response(
            status_code=status_code,
            json=response_data if response_data is not None else [],
            request=request
        )

    return httpx.MockTransport(mock_github_response)


# Test the root and health endpoints.
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to GitHub Gist API"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# Test the assignment's required octocat scenario.
# The GitHub API response is mocked using HTTPX MockTransport.
# The original GitHub client function is retained, but the mock
# transport is passed to it instead of making a real network call.
# The route's reference to fetch_user_gists is temporarily patched
# so the test can verify the complete API request and response flow.
def test_get_octocat_gists():
    transport = create_mock_transport(
        status_code=200,
        response_data=MOCK_GISTS
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
        response = client.get("/octocat")

    assert response.status_code == 200

    gists = response.json()
    assert isinstance(gists, list)
    assert len(gists) == 2
    assert gists[0]["id"] == "12345"
    assert gists[0]["public"] is True
    assert gists[1]["id"] == "67890"


# Test handling of an unknown GitHub user.
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


# Test handling of a GitHub API request timeout.
def test_github_request_timeout():
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
