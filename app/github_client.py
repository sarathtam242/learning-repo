import logging
import httpx
from app.config import settings

logger = logging.getLogger(__name__)


# Fetch public GitHub Gists for a given username.
async def fetch_user_gists(username: str, transport=None):
    github_url = f"{settings.github_api_base_url}/users/{username}/gists"
    logger.info("Fetching public Gists for username: %s", username)

    try:
        async with httpx.AsyncClient(
            timeout=settings.request_timeout,
            transport=transport
        ) as client:
            response = await client.get(github_url)
            response.raise_for_status()
            gists = response.json()

            logger.info(
                "Successfully fetched %d Gists for username: %s",
                len(gists),
                username
            )
            return gists

    except httpx.TimeoutException:
        logger.error("GitHub API request timed out for username: %s", username)
        raise

    except httpx.HTTPStatusError as exc:
        logger.error(
            "GitHub API returned status %d for username: %s",
            exc.response.status_code,
            username
        )
        raise

    except httpx.RequestError:
        logger.exception("Unable to communicate with GitHub API for username: %s", username)
        raise
