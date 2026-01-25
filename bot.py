from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "7643831340:AAGieuPJND4MekAutSf3xzta1qdoKo5mbZU"

dice_words = {
    1: "ONE",
    2: "TWO",
    3: "THREE",
    4: "FOUR",
    5: "FIVE",
    6: "SIX"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎲 Dice Bot Ready!\n\n"
        "Command use karo:\n"
        "/dice"
    )

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dice_msg = await update.message.reply_dice(emoji="🎲")
    value = dice_msg.dice.value

    await update.message.reply_text(
        f"🎲 Dice Rolled!\n"
        f"Number: {value}\n"
        f"Word: {dice_words[value]}"
    )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("dice", dice))

print("Dice bot running...")
app.run_polling()
