from fastapi import FastAPI
from app.routers import mysql_generic, mongo_generic

app = FastAPI(title="Multi-DB FastAPI")

# Include the generic CRUD routers
app.include_router(mysql_generic.router)
app.include_router(mongo_generic.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Multi-DB FastAPI environment!"}
