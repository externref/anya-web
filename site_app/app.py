from __future__ import annotations

import os
import pathlib
import secrets
import uuid

import aiofiles
import dotenv
import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import db_handler, discord_rest, html_creator

dotenv.load_dotenv()
app = fastapi.FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=pathlib.Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)
app.mount(
    "/assets",
    StaticFiles(directory=pathlib.Path(__file__).parent.parent.absolute() / "assets"),
    name="assets",
)
templates = Jinja2Templates(directory="static")


@app.on_event("startup")
async def _():
    if not db_handler.database.is_connected:
        await db_handler.database.connect()


@app.get("/home")
@app.get("/", response_class=fastapi.responses.HTMLResponse)
async def home(request: fastapi.Request):
    try:
        await _()
        async with aiofiles.open("static/home.html") as file:
            data = await file.read()
        if oauth := await db_handler.database.get_oauth(
            request.cookies.get("session_id")
        ):
            print(1)
            user = await discord_rest.fetch_user(oauth)
            data = data.replace(
                """class="glyphicon glyphicon-log-in" href="./login""",
                """style="font-family: Rockwell Extra Bold, Rockwell Bold, monospace;" href="./dashboard""",
            ).replace(
                "Login",
                f"""<img class="img-circle" src="{user.display_avatar_url}" style="height: 30px;width:30px;"> {str(user)}""",
            )
        res = fastapi.responses.HTMLResponse(data)
        if not auth:
            res.set_cookie("session_id", uuid.uuid4())
        return res
    except Exception as e:
        print(e)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return fastapi.responses.FileResponse("static/favicon.ico")


@app.get("/login")
async def login(request: fastapi.Request):
    try:
        if await db_handler.database.pool.fetchval(
            "SELECT * FROM login_data WHERE session_id = $1",
            (s_id := request.cookies.get("session_id")),
        ):
            res = fastapi.responses.RedirectResponse("/dashboard")
            res.set_cookie("session_id", s_id)
            return res
        res = fastapi.responses.RedirectResponse(
            "https://discord.com/api/oauth2/authorize?client_id=979906554188939264&redirect_uri=https%3A%2F%2Fanyaa.ml%2Fauth&response_type=code&scope=identify%20guilds"
        )
        res.set_cookie("session_id", uuid.uuid4())
        return res
    except Exception as e:
        print(e)


@app.get("/auth/")
async def auth(request: fastapi.Request, code: str):

    if not request.cookies.get("session_id"):
        return fastapi.responses.RedirectResponse("/")
    try:
        print(request.cookies)
        await discord_rest.register_login(request.cookies["session_id"], code)
        res = fastapi.responses.RedirectResponse(
            "/dashboard",
        )
        res.set_cookie("session_id", request.cookies["session_id"])
        return res
    except Exception as e:
        print(e)


@app.get("/dashboard")
async def dash(request: fastapi.Request):

    if not request.cookies.get("session_id"):
        return fastapi.responses.RedirectResponse("/")
    try:
        print(request.cookies)
        if await db_handler.database.pool.fetchval(
            "SELECT * FROM login_data WHERE session_id = $1",
            (s_id := request.cookies["session_id"]),
        ):
            oauth = await db_handler.database.get_oauth(s_id)
            res = fastapi.responses.HTMLResponse(
                await html_creator.create_user_profile_tag(
                    await discord_rest.fetch_user(oauth)
                )
                + await html_creator.add_guilds(await discord_rest.fetch_guilds(oauth))
            )
            res.set_cookie("session_id", request.cookies["session_id"])
            return res
        else:
            return fastapi.responses.RedirectResponse(
                "https://discord.com/api/oauth2/authorize?client_id=979906554188939264&redirect_uri=https%3A%2F%2Fanyaa.ml%2Fauth&response_type=code&scope=identify%20guilds"
            )
    except Exception as e:
        print(e)


@app.get("/logout")
async def logout(request: fastapi.Request):

    if not request.cookies.get("session_id"):
        return fastapi.responses.RedirectResponse("/")
    await db_handler.database.pool.execute(
        "DELETE from login_data WHERE session_id = $1", request.cookies["session_id"]
    )
    return fastapi.responses.RedirectResponse("/home")
