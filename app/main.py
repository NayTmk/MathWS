from fastapi import FastAPI
from app.routers import main_pages, users, login, game


app = FastAPI()
app.include_router(main_pages.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(game.router)