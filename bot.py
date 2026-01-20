from telethon import TelegramClient, events
import asyncio

api_id = 123456      # my.telegram.org se
api_hash = "API_HASH_HERE"
session = "slot_userbot"

client = TelegramClient(session, api_id, api_hash)

TARGET_CHAT = -1001234567890  # group / channel id
SLOT_EMOJI = "🎰"
RUN = False

@client.on(events.NewMessage(pattern="/startslot"))
async def start_slot(event):
    global RUN
    RUN = True
    await event.reply("🎰 Slot started, waiting for 777...")
    while RUN:
        msg = await client.send_message(TARGET_CHAT, SLOT_EMOJI)
        await asyncio.sleep(1.8)  # timing is IMPORTANT

@client.on(events.NewMessage)
async def check_result(event):
    global RUN
    if event.message.dice:
        value = event.message.dice.value
        if value == 64:  # 🎰 ka jackpot value (777)
            RUN = False
            await event.reply("🔥 JACKPOT 777 HIT! STOPPED 🔥")

@client.on(events.NewMessage(pattern="/stopslot"))
async def stop_slot(event):
    global RUN
    RUN = False
    await event.reply("❌ Slot stopped")

client.start()
client.run_until_disconnected()
