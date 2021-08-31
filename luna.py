import re
import os
from asyncio import gather, get_event_loop, sleep

from aiohttp import ClientSession
from pyrogram import Client, filters, idle
from Python_ARQ import ARQ

bot_token = "1964873608:AAFR2nWYJORCfoSjJfGB5x_vEQE__PjFdEM"
ARQ_API_KEY = "PIHVJY-TCWRTN-FRGUHB-QOUFXH-ARQ"
ARQ_API_BASE_URL = "https://thearq.tech"
LANGUAGE = "en"

luna = Client(
    ":memory:",
    bot_token=bot_token,
    api_id=2344247 ,
    api_hash="853cae451f8091db916cd9ad395bbf12",
)

bot_id = int(bot_token.split(":")[0])
arq = None

async def lunaQuery(query: str, user_id: int):
    query = (
        query
        if LANGUAGE == "en"
        else (await arq.translate(query, "en")).result.translatedText
    )
    resp = (await arq.luna(query, user_id)).result
    return (
        resp
        if LANGUAGE == "en"
        else (
            await arq.translate(resp, LANGUAGE)
        ).result.translatedText
    )


async def type_and_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(2))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, "cancel")


@luna.on_message(
    ~filters.private
    & filters.text
    & ~filters.command("help")
    & ~filters.edited,
    group=69,
)
async def chat(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        from_user_id = message.reply_to_message.from_user.id
        if from_user_id != bot_id:
            return
    else:
        match = re.search(
            "[.|\n]{0,}rias[.|\n]{0,}",
            message.text.strip(),
            flags=re.IGNORECASE,
        )
        if not match:
            return
    await type_and_send(message)

async def main():
    global arq
    session = ClientSession()
    arq = ARQ(ARQ_API_BASE_URL, ARQ_API_KEY, session)

    await luna.start()
    print(
        """
-----------------
| Rias Started! |
-----------------
"""
    )
    await idle()


loop = get_event_loop()
loop.run_until_complete(main())
