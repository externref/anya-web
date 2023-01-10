import os

import hikari

bot = hikari.RESTApp()
bot_running = False
user_token_map: dict[int, str] = {}
user_object_map: dict[int, hikari.User] = {}


async def get_oauth(code: str) -> hikari.OAuth2AuthorizationToken:
    async with bot.acquire(None) as rest:
        auth = await rest.authorize_access_token(
            979906554188939264,
            os.environ["CLIENT_SECRENT"],
            code,
            "https://anya.deta.dev/auth",
        )
        return auth


async def get_id_from_code(code: str) -> str:
    global bot_running
    if bot_running is False:
        await bot.start()
        bot_running = True
    auth = await get_oauth(code)
    async with bot.acquire(auth.access_token, auth.token_type) as rest:

        user = await rest.fetch_my_user()
    user_token_map[user.id] = auth.access_token
    user_object_map[user.id] = user
    return user.id
