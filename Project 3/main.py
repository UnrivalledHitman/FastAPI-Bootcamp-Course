from fastapi import FastAPI
from database import engine, SessionLocal, base
from routers import auth, todos

app = FastAPI()

# Creates the database tables based on your models
base.metadata.create_all(bind=engine)

# Creating the routers
app.include_router(auth.router)
app.include_router(todos.router)
