import logging
import httpx

from app.config import settings


# Create a logger for this module.
logger = logging.getLogger(__name__)


async def fetch_user_gists(username: str, transport=None):
    """
    Fetch publicly available Gists for a GitHub username.
    """

    # Construct the GitHub API URL.
    github_url = f"{settings.github_api_base_url}/users/{username}/gists"

    logger.info("Fetching public Gists for username: %s", username)

    try:
        # Create an asynchronous HTTP client with the configured timeout.
        async with httpx.AsyncClient(
            timeout=settings.request_timeout,
            transport=transport
        ) as client:

            # Send a GET request to GitHub.
            response = await client.get(github_url)

            # Raise an exception for HTTP 4xx or 5xx responses.
            response.raise_for_status()

            # Convert the JSON response into Python data.
            gists = response.json()

            logger.info(
                "Successfully fetched %d Gists for username: %s",
                len(gists),
                username
            )

            return gists

    except httpx.TimeoutException:
        logger.error(
            "GitHub API request timed out for username: %s",
            username
        )
        raise

    except httpx.HTTPStatusError as exc:
        logger.error(
            "GitHub API returned status %d for username: %s",
            exc.response.status_code,
            username
        )
        raise

    except httpx.RequestError:
        logger.exception(
            "Unable to communicate with GitHub API for username: %s",
            username
        )
        raise
