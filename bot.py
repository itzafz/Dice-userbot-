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

BOT_TOKEN = "8155211870:AAHk1E1F98hT5P8OfQB_w_zyLl6IXZjtBEY"

games = {}  # message_id : game data


def board_markup(board):
    kb = []
    for i in range(0, 9, 3):
        kb.append([
            InlineKeyboardButton(board[i], callback_data=str(i)),
            InlineKeyboardButton(board[i+1], callback_data=str(i+1)),
            InlineKeyboardButton(board[i+2], callback_data=str(i+2)),
        ])
    return InlineKeyboardMarkup(kb)


def winner(b):
    win = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for x,y,z in win:
        if b[x] == b[y] == b[z] != "⬜":
            return True
    return False


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="🎮 Start XOXO Game",
        description="Inline Tic-Tac-Toe game",
        input_message_content=InputTextMessageContent(
            "❌ **XOXO Game Started!**\nPlayer ❌ turn"
        ),
        reply_markup=board_markup(["⬜"] * 9)
    )
    await update.inline_query.answer([result], cache_time=0)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    msg_id = query.message.message_id

    if msg_id not in games:
        games[msg_id] = {
            "board": ["⬜"] * 9,
            "turn": "❌"
        }

    game = games[msg_id]
    idx = int(query.data)

    if game["board"][idx] != "⬜":
        return

    game["board"][idx] = game["turn"]

    if winner(game["board"]):
        await query.edit_message_text(
            f"🏆 **{game['turn']} wins!**",
            reply_markup=board_markup(game["board"]),
            parse_mode="Markdown"
        )
        games.pop(msg_id)
        return

    if "⬜" not in game["board"]:
        await query.edit_message_text(
            "🤝 **Draw!**",
            reply_markup=board_markup(game["board"]),
            parse_mode="Markdown"
        )
        games.pop(msg_id)
        return

    game["turn"] = "⭕" if game["turn"] == "❌" else "❌"

    await query.edit_message_reply_markup(
        reply_markup=board_markup(game["board"])
    )


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(InlineQueryHandler(inline_query))
app.add_handler(CallbackQueryHandler(button))

print("Inline XOXO Bot Running...")
app.run_polling()
