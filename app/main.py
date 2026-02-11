from fastapi import FastAPI

from app.core.router import router

app = FastAPI()

app.include_router(router)
