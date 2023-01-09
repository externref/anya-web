import pathlib
import os
import secrets
import aiofiles
import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import discord_rest, html_creator

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


@app.get("/", response_class=fastapi.responses.HTMLResponse)
async def home(request: fastapi.Request):
    async with aiofiles.open("static/home.html") as file:
        data =await file.read()
        data=data.replace("$bg_image", secrets.choice(os.listdir("assets/backgrounds")))
    return fastapi.responses.HTMLResponse(data)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return fastapi.responses.FileResponse("static/favicon.ico")


@app.get("/login")
async def login():
    return fastapi.responses.RedirectResponse(
        "https://discord.com/api/oauth2/authorize?client_id=979906554188939264&redirect_uri=https%3A%2F%2Fanya.deta.dev%2Fauth&response_type=code&scope=identify"
    )


@app.get("/auth/")
async def auth(code: str):
    try:
        _id = await discord_rest.get_id_from_code(code)
    except Exception as e:
        print(e)
    return fastapi.responses.RedirectResponse(f"/dashboard/{_id}")


@app.get("/dashboard/{user_id}")
async def dash(user_id: int):
    
    try:

        return fastapi.responses.HTMLResponse(html_creator.create_user_profile_tag(discord_rest.user_object_map[user_id]))
    except KeyError:
        return fastapi.responses.RedirectResponse(
        "https://discord.com/api/oauth2/authorize?client_id=979906554188939264&redirect_uri=https%3A%2F%2Fanya.deta.dev%2Fauth&response_type=code&scope=identify"
    )
        
@app.get("/logout/{user_id}")
async def logout(user_id: int ):
    discord_rest.user_object_map.pop(user_id)
    return fastapi.responses.RedirectResponse("/home")

