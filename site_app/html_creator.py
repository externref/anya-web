from __future__ import annotations

import os
import secrets

import aiofiles
import hikari

from . import discord_rest

url_map = {
    "Invite Bot": "https://discord.com/api/oauth2/authorize?client_id=979906554188939264&permissions=516020358208&scope=bot%20applications.commands",
    "Support Server": "https://discord.com/invite/FyEE54u9GF",
}


async def create_user_profile_tag(user: hikari.OwnUser = None) -> str:

    async with aiofiles.open("static/profile.html") as file:
        doc = await file.read()
    [
        doc := doc.replace(old, new)
        for old, new in {
            "$bg_image": "../assets/backgrounds/"
            + secrets.choice(os.listdir("assets/backgrounds")),
            "$user_id": str(user.id),
            "$user_name": user.username,
            "$user_discrim": user.discriminator,
            "$avatar": user.display_avatar_url.url,
            "$created_at": user.created_at.strftime("%d-%B-%y"),
        }.items()
    ]
    return doc


async def add_guilds(guilds: list[hikari.OwnGuild]) -> str:
    async with aiofiles.open("static/guild_temp.html") as file:
        temp = await file.read()
    txt = ""
    bot_guilds = await discord_rest.fetch_bot_guilds()
    for guild in guilds:
        if guild in bot_guilds and (
            guild.my_permissions & hikari.Permissions.MANAGE_GUILD
        ):
            txt += (
                temp.replace("$guild_name", guild.name)
                .replace(
                    "$guild_icon",
                    str(guild.icon_url)
                    if guild.icon_url
                    else "https://cdn.discordapp.com/embed/avatars/0.png",
                )
                .replace("$forward_url", f"manage/{guild.id}")
                .replace("$text", "Manage")
                .replace("$gly", "cog")
            )
    for guild in guilds:
        if guild not in bot_guilds and (
            guild.my_permissions & hikari.Permissions.MANAGE_GUILD
        ):
            txt += (
                temp.replace("$guild_name", guild.name)
                .replace(
                    "$guild_icon",
                    str(guild.icon_url)
                    if guild.icon_url
                    else "https://cdn.discordapp.com/embed/avatars/0.png",
                )
                .replace("$forward_url", f"-")
                .replace("$text", "Add bot")
                .replace("$gly", "plus")
            )

    return txt + "</body></html>"


async def manage_page(guild: hikari.Guild) -> str:
    async with aiofiles.open("static/manage.html") as file:
        data = await file.read()

    return (
        data.replace(
            "$guild_icon",
            str(guild.icon_url)
            if guild.icon_url
            else "https://cdn.discordapp.com/embed/avatars/0.png",
        )
        .replace("$guild_id", str(guild.id))
        .replace("$guild", guild.name)
        .replace("$created_at", guild.created_at.strftime("%d-%B-%y"))
    )
