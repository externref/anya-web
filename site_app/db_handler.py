from __future__ import annotations

import aiofiles
import asyncpg
import os
import hikari
import attrs


@attrs.define(kw_only=True)
class OauthRecord:
    user_id: int
    session_id: int
    access_token: str | None
    refresh_token: str | None
    token_type: str


class Database:
    is_connected: bool = False
    pool: asyncpg.Pool

    async def connect(self) -> None:
        self.is_connected = True
        self.pool = await asyncpg.create_pool(os.environ["PGSQL_URL"])
        async with aiofiles.open("sql_config.sql") as file:
            for squery in (await file.read()).split("\n\n"):
                print(squery)
                await self.pool.execute(squery)

    async def enter_oauth_data(
        self, uid: int, session_id: str, data: hikari.OAuth2AuthorizationToken
    ) -> None:
        await self.pool.execute(
            "INSERT INTO login_data VALUES ( $1, $2, $3, $4, $5 ) ON CONFLICT DO NOTHING",
            uid,
            session_id,
            data.access_token,
            data.refresh_token,
            str(data.token_type),
        )

    async def get_oauth(self, session_id: str) -> OauthRecord:
        return (
            OauthRecord(**data)
            if (
                data := await self.pool.fetchrow(
                    "SELECT * FROM login_data WHERE session_id = $1", session_id
                )
            )
            is not None
            else None
        )


database = Database()
