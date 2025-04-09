from fastapi import FastAPI
from app.auth_service import routers as auth_router
from app.post_service import routers as post_router
from fastapi.openapi.utils import get_openapi
from app.db import database

app = FastAPI(title="Mini Blog API")
database.Base.metadata.create_all(bind=database.engine)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="API with autorization",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", []).append({"OAuth2PasswordBearer": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(auth_router.router)
app.include_router(post_router.router)