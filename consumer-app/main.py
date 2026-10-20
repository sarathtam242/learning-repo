
from fastapi import FastAPI
from health_utils import is_healthy

app = FastAPI()


@app.get("/health/{status_code}")
def check_health(status_code: int):
    return {
        "status_code": status_code,
        "healthy": is_healthy(status_code)
    }
