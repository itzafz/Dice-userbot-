from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = 24526311
api_hash = "717d5df262e474f88d86c537a787c98d"
string_session = "BQF2PecAeTUNNzoR0brOdxB_SQtDNxT-sOc1A1giDUQPANuGOoyNgNpQnnmnaWckd_MV4DPsdTAJFLtxsRcPBOuyt81hRaUX5J2ZVDLiA-Zb2ZwaoXkynFmNwzV6MHxEBEGU96aC91mGelD79eyXXTosavkb8EmzhGXkriF1hxGBcbI-cEfYQnNvkNyTr5vX-ZzDnE6lOsDzO_UnarAwqVpXyfdnNI5bdHf2blMQ2mCcVRS4wtFTBhYayhwEKFugYg3nWKdSbzDZ9x_AJ5ZVi_goMziq_flv2BWVg28pHOz4yVqBzxuluP7nc5etUX7TKwKFgu8rur7qJeLDV09iciAeZWxKEgAAAAHwVWW1AA"

client = TelegramClient(
    StringSession(string_session),
    api_id,
    api_hash
)

@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    text = event.raw_text.lower()

    if text == "ping":
        await event.reply("pong")

    elif text == "dice":
        await event.reply("🎲")

client.start()
client.run_until_disconnected()
