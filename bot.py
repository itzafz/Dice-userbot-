from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎲 Dice Bot Ready!\n\n"
        "Inline use karo:\n"
        "@YourBotUsername"
    )

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query

    result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="🎲 Roll Dice",
        description="Tap to roll a dice",
        input_message_content=InputTextMessageContent(
            "🎲 Rolling Dice..."
        )
    )

    await query.answer([result], cache_time=0)

async def handle_inline_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if message.text == "🎲 Rolling Dice...":
        dice_msg = await message.reply_dice(emoji="🎲")
        value = dice_msg.dice.value

        await message.reply_text(
            f"🎲 Dice Rolled!\n"
            f"Number: {value}\n"
            f"Word: {dice_words[value]}"
        )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(InlineQueryHandler(inline_query))
app.add_handler(CommandHandler(None, handle_inline_message))

print("Inline Dice Bot running...")
app.run_polling()
