import logging
import os
import sys
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from prometheus_client import Counter, Gauge, Histogram, Info
from prometheus_fastapi_instrumentator import Instrumentator
from routers import (
    download_router,
    orbit_families_router,
    orbit_poincare_view_router,
    orbit_view_router,
    trajectory_points_router,
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("app.log")],
)

logger = logging.getLogger(__name__)


app = FastAPI(title="Orbit Catalog Backend Service")


HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests in progress",
    ["method", "endpoint", "app_name"],
)

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total count of HTTP requests",
    ["method", "endpoint", "status_code", "app_name"],
)

HTTP_REQUESTS_DURATION_SECONDS = Histogram(
    "http_requests_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint", "status_code", "app_name"],
    buckets=[0.1, 0.5, 1, 2, 5, 10],
)

HTTP_EXCEPTIONS_TOTAL = Counter(
    "http_exceptions_total",
    "Total count of HTTP exceptions",
    ["method", "endpoint", "exception_type", "app_name"],
)

HTTP_RESPONSES_TOTAL = Counter(
    "http_responses_total",
    "Total count of HTTP responses",
    ["method", "endpoint", "status_code", "app_name"],
)


instrumentator = Instrumentator(
    should_instrument_requests_inprogress=False,
    should_group_status_codes=False,
    should_ignore_untemplated=True,
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)

    method = request.method
    endpoint = request.url.path
    app_name = "orbit-catalog-backend"

    HTTP_REQUESTS_IN_PROGRESS.labels(
        method=method, endpoint=endpoint, app_name=app_name
    ).inc()

    start_time = time.time()

    try:
        response = await call_next(request)
        status_code = response.status_code

        duration = time.time() - start_time

        HTTP_REQUESTS_TOTAL.labels(
            method=method, endpoint=endpoint, status_code=status_code, app_name=app_name
        ).inc()

        HTTP_REQUESTS_DURATION_SECONDS.labels(
            method=method, endpoint=endpoint, status_code=status_code, app_name=app_name
        ).observe(duration)

        HTTP_RESPONSES_TOTAL.labels(
            method=method, endpoint=endpoint, status_code=status_code, app_name=app_name
        ).inc()

        return response

    except Exception as e:
        # Обработка исключений
        exception_type = type(e).__name__
        status_code = 500

        HTTP_EXCEPTIONS_TOTAL.labels(
            method=method,
            endpoint=endpoint,
            exception_type=exception_type,
            app_name=app_name,
        ).inc()

        HTTP_REQUESTS_TOTAL.labels(
            method=method, endpoint=endpoint, status_code=status_code, app_name=app_name
        ).inc()

        HTTP_RESPONSES_TOTAL.labels(
            method=method, endpoint=endpoint, status_code=status_code, app_name=app_name
        ).inc()

        raise e

    finally:
        # Уменьшаем счетчик in-progress
        HTTP_REQUESTS_IN_PROGRESS.labels(
            method=method, endpoint=endpoint, app_name=app_name
        ).dec()


instrumentator.instrument(app)


instrumentator.expose(app, endpoint="/metrics", include_in_schema=False)


fastapi_app_info = Info("fastapi_app_info", "FastAPI application info")
fastapi_app_info.info({"app_name": "orbit-catalog-backend", "version": "1.0.0"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

app.include_router(trajectory_points_router)
app.include_router(orbit_view_router)
app.include_router(orbit_poincare_view_router)
app.include_router(orbit_families_router)
app.include_router(download_router)

frontend_path = "front"
index_html_path = f"{frontend_path}/index.html"

if os.path.exists(index_html_path):
    print("Frontend found, setting up static files...")

    if os.path.exists(f"{frontend_path}/assets"):
        app.mount(
            "/assets", StaticFiles(directory=f"{frontend_path}/assets"), name="assets"
        )

    @app.get("/")
    async def read_index():
        return FileResponse(index_html_path)

    @app.get("/{path:path}")
    async def catch_all(path: str):
        if path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")

        full_path = f"{frontend_path}/{path}"
        if os.path.exists(full_path) and os.path.isfile(full_path):
            return FileResponse(full_path)

        return FileResponse(index_html_path)

else:
    print("Frontend not found. Please build the frontend with 'npm run build'")

    @app.get("/")
    async def root():
        return {
            "message": "Frontend is not built. Run 'npm run build' in front directory."
        }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app:app", port=8000, reload=True)
