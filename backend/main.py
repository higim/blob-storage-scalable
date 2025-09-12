from fastapi import FastAPI
from api import router

app = FastAPI(title="Streaming Music API")
app.include_router(router)