from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent
)
from telegram.ext import (
    ApplicationBuilder,
    InlineQueryHandler,
    CallbackQueryHandler,
    ContextTypes
)
import uuid
import logging

BOT_TOKEN = "8155211870:AAHk1E1F98hT5P8OfQB_w_zyLl6IXZjtBEY"

logging.basicConfig(level=logging.INFO)

# inline_message_id / message_id : game data
games = {}


def make_board(board):
    keyboard = []
    for i in range(0, 9, 3):
        keyboard.append([
            InlineKeyboardButton(board[i], callback_data=str(i)),
            InlineKeyboardButton(board[i+1], callback_data=str(i+1)),
            InlineKeyboardButton(board[i+2], callback_data=str(i+2)),
        ])
    return InlineKeyboardMarkup(keyboard)


def check_win(b):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for x, y, z in wins:
        if b[x] == b[y] == b[z] != "⬜":
            return True
    return False


# INLINE QUERY HANDLER
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="🎮 Start XOXO Game",
        description="Play Tic-Tac-Toe inline",
        input_message_content=InputTextMessageContent(
            "❌ **XOXO Game Started**\nTurn: ❌",
            parse_mode="Markdown"
        ),
        reply_markup=make_board(["⬜"] * 9)
    )
    await update.inline_query.answer([result], cache_time=0)


# BUTTON HANDLER
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # INLINE FIX (MOST IMPORTANT)
    game_id = query.inline_message_id or query.message.message_id

    if game_id not in games:
        games[game_id] = {
            "board": ["⬜"] * 9,
            "turn": "❌"
        }

    game = games[game_id]
    index = int(query.data)

    if game["board"][index] != "⬜":
        return

    game["board"][index] = game["turn"]

    # WIN
    if check_win(game["board"]):
        await query.edit_message_text(
            f"🏆 **{game['turn']} Wins!**",
            reply_markup=make_board(game["board"]),
            parse_mode="Markdown"
        )
        games.pop(game_id, None)
        return

    # DRAW
    if "⬜" not in game["board"]:
        await query.edit_message_text(
            "🤝 **Match Draw!**",
            reply_markup=make_board(game["board"]),
            parse_mode="Markdown"
        )
        games.pop(game_id, None)
        return

    # NEXT TURN
    game["turn"] = "⭕" if game["turn"] == "❌" else "❌"

    await query.edit_message_reply_markup(
        reply_markup=make_board(game["board"])
    )


# APP START
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(InlineQueryHandler(inline_query))
app.add_handler(CallbackQueryHandler(button_handler))

print("✅ Inline XOXO Bot Running...")
app.run_polling()
