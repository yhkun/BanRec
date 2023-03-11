from pagermaid.listener import listener
from pagermaid.enums import Message
from pagermaid.enums import Client
from pyrogram.raw import functions, types
import asyncio


@listener(command="rec",
          description="自动批量封禁表态用户",
          usage="直接回复一条被表态的消息即可")
async def recstart(message: Message,client:Client):
    try:
        grpid = await client.resolve_peer(message.chat.id)
        megg = await client.invoke(
            functions.messages.GetMessageReactionsList(
                peer=grpid,
                id=message.reply_to_message_id,
                limit=100
                )
            )
    except:
        return await message.edit("无法获取表态列表。")
    
    users = megg.users
    uidl = []
    for x in users:
        uidl.append(x.id)
    await message.edit("表态用户获取成功，开始自动封禁...")
    str1 = ""
    for y in uidl:
        try:
            await client.ban_chat_member(message.chat.id,y)
            str1 = str1 + f"[{y}](tg://user?id={y}) 封禁成功\n"
        except:
            str1 = str1 + f"[{y}](tg://user?id={y}) 封禁失败\n"
        await asyncio.sleep(1)
        await message.edit(str1)
