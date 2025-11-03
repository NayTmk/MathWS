from fastapi import FastAPI

from app.routers import users
from app.routers import game, gamesessions, login


def create_app():
    app = FastAPI()

    app.include_router(users.router)
    app.include_router(gamesessions.router)
    app.include_router(login.router)
    app.include_router(game.router)

    return app

app = create_app()