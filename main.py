import os

import uvicorn
from fastapi import FastAPI, HTTPException, status, Security, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security.api_key import APIKey, APIKeyQuery, APIKeyHeader, APIKeyCookie
from starlette.responses import HTMLResponse, JSONResponse
from starlette.responses import RedirectResponse

from utils import detect_labels_uri

API_KEY = os.environ.get('KEY')
API_KEY_NAME = "key"
COOKIE_DOMAIN = os.environ.get('COOKIE_DOMAIN')

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


async def get_api_key(
        api_key_query: str = Security(api_key_query),
        api_key_header: str = Security(api_key_header),
        api_key_cookie: str = Security(api_key_cookie),
):
    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


@app.get("/")
async def homepage():
    return HTMLResponse(
        "<h1>Welcome to the AutoMagic HashTag app !" \
        " Soon you will be able generate HashTags for Photos simply and fast by upload it or share a URL</h1>"
    )


@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response


@app.get("/openapi.json", tags=["documentation"], include_in_schema=False)
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = JSONResponse(
        get_openapi(title="Automagic HashTag API Documentation", version=1, routes=app.routes)
    )
    return response


@app.get("/docs", tags=["documentation"])
async def get_documentation(api_key: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        API_KEY_NAME,
        value=api_key,
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response


@app.get("/api/")
async def get_hashtags_by_url(url: str, api_key: APIKey = Depends(get_api_key)):
    hash_tags = detect_labels_uri(url)
    return {"hash_tags": hash_tags}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
