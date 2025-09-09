from fastapi import FastAPI
from api import router
from consumer import start_consumer_thread

app = FastAPI(title="Streaming Music API")
app.include_router(router)

start_consumer_thread()