from fastapi import FastAPI
from routers import mahasiswa

app = FastAPI()

app.include_router(mahasiswa.router)