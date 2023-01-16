from __future__ import annotations

import os

import hikari

from .db_handler import database, OauthRecord

bot = hikari.RESTApp()
bot_running = False


async def get_oauth(code: str) -> hikari.OAuth2AuthorizationToken:
    async with bot.acquire(None) as rest:
        auth = await rest.authorize_access_token(
            979906554188939264,
            os.environ["CLIENT_SECRET"],
            code,
            "https://anyaa.ml/auth",
        )

        return auth


async def _check() -> None:
    global bot_running
    if bot_running is False:
        await bot.start()
        bot_running = True


async def register_login(session_id: str, code: str) -> str:
    await _check()
    auth = await get_oauth(code)
    async with bot.acquire(auth.access_token, auth.token_type) as rest:

        user = await rest.fetch_my_user()
    await database.enter_oauth_data(user.id, session_id, auth)


async def fetch_user(oauth: OauthRecord) -> hikari.OwnUser:
    await _check()
    async with bot.acquire(oauth.access_token, oauth.token_type) as rest:
        return await rest.fetch_my_user()

async def fetch_guild(oauth: OauthRecord, g_id: int) -> hikari.OwnGuild:
    await _check()
    async with bot.acquire(os.environ['BOT_TOKEN'], hikari.TokenType.BOT) as rest:
        return await rest.fetch_guild(g_id)

async def fetch_guilds(oauth: OauthRecord) -> list[hikari.OwnGuild]:

    await _check()
    async with bot.acquire(oauth.access_token, oauth.token_type) as rest:
        return await rest.fetch_my_guilds()


async def fetch_bot_guilds() -> list[hikari.OwnGuild]:
    await _check()
    async with bot.acquire(os.environ["BOT_TOKEN"], hikari.TokenType.BOT) as rest:
        return await rest.fetch_my_guilds()
