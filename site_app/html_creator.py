import os
import secrets

import aiofiles
import hikari

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
    print(doc)
    return doc
