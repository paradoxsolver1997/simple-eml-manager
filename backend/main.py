from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.api import router


app = FastAPI(title="EML Search")

# API
app.include_router(router)

# Frontend (serve index.html)
app.mount(
    "/", 
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)
