from fastapi import FastAPI
from app.api.routes import router
from app.core.scheduler import dummy, start_scheduler
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, POST, etc.
    allow_headers=["*"], # Allows all headers
)

app.include_router(router)

@app.on_event("startup")
async def startup():
    # dummy()
    start_scheduler()