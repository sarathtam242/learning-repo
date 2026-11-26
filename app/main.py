import logging
from fastapi import FastAPI
from app.config import settings
from app.routes import router


# Configure application-wide logging.
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

app = FastAPI(
    title="GitHub Gist API",
    description="API to retrieve public GitHub Gists",
    version="1.0.0"
)

app.include_router(router)
