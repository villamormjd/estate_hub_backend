from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from src.routes.user import user
from src.routes.property import prop
from src.routes.unit import unit

#Initiating App Object
app = FastAPI(
    title="Estate Hub"
)

app.include_router(user)
app.include_router(prop)
app.include_router(unit)

origins = ['https://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def status():
    return RedirectResponse("/docs")
