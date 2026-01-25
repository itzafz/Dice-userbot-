from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
    MessageHandler,
    filters
)
import uuid

BOT_TOKEN = "7643831340:AAGieuPJND4MekAutSf3xzta1qdoKo5mbZU"

dice_words = {
    1: "ONE",
    2: "TWO",
    3: "THREE",
    4: "FOUR",
    5: "FIVE",
    6: "SIX"
}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎲 Dice Bot Ready\n\n"
        "Inline use:\n"
        "@YourBotUsername\n\n"
        "Ya /dice command use karo"
    )

# normal /dice command
async def dice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dice_msg = await update.message.reply_dice(emoji="🎲")
    value = dice_msg.dice.value

    await update.message.reply_text(
        f"🎲 Dice Rolled!\n"
        f"Number: {value}\n"
        f"Word: {dice_words[value]}"
    )

# inline query handler
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="🎲 Roll Dice",
        description="Send a dice",
        input_message_content=InputTextMessageContent(
            "🎲 Rolling Dice..."
        )
    )
    await update.inline_query.answer([result], cache_time=0)

# handle inline sent message
async def handle_inline_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    # safety check
    if not message.text:
        return

    if message.text != "🎲 Rolling Dice...":
        return

    dice_msg = await message.reply_dice(emoji="🎲")
    value = dice_msg.dice.value

    await message.reply_text(
        f"🎲 Dice Rolled!\n"
        f"Number: {value}\n"
        f"Word: {dice_words[value]}"
    )

# app setup
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("dice", dice_cmd))
app.add_handler(InlineQueryHandler(inline_query))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_inline_message))

print("✅ Dice Bot Running...")
app.run_polling()
