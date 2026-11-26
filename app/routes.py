import logging
import httpx
from fastapi import APIRouter, HTTPException
from app.github_client import fetch_user_gists

logger = logging.getLogger(__name__)
router = APIRouter()


# Application health-check endpoint.
@router.get("/health")
async def health_check():
    return {"status": "healthy"}


# Root endpoint providing basic API information.
@router.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to GitHub Gist API",
        "usage": "Use /{username} to retrieve public GitHub Gists",
        "example": "/octocat"
    }


# Retrieve public Gists and handle GitHub API errors.
@router.get("/{username}")
async def get_user_gists(username: str):
    try:
        return await fetch_user_gists(username)

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="GitHub API request timed out"
        )

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="GitHub user not found"
            )
        raise HTTPException(
            status_code=502,
            detail="GitHub API returned an error"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Unable to communicate with GitHub API"
        )
