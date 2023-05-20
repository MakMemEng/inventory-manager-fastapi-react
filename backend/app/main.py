from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import materials, inventories
from api.materials import insert_test_data
from database import Base, engine

# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(materials.router)
app.include_router(inventories.router)

# @app.on_event("startup")
# async def startup_event():
#     insert_test_data()
