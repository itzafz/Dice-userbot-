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

BOT_TOKEN = "8425346293:AAGd2Z5eG8clPMODe7ker8LqIBN4KFoioQw"

logging.basicConfig(level=logging.INFO)

games = {}  # game_id : data


def board_markup(board):
    kb = []
    for i in range(0, 9, 3):
        kb.append([
            InlineKeyboardButton(board[i], callback_data=str(i)),
            InlineKeyboardButton(board[i+1], callback_data=str(i+1)),
            InlineKeyboardButton(board[i+2], callback_data=str(i+2)),
        ])
    return InlineKeyboardMarkup(kb)


def check_win(b):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for x,y,z in wins:
        if b[x] == b[y] == b[z] != "⬜":
            return True
    return False


def game_text(game):
    p = game["players"]
    if len(p) == 2:
        return f"❌ {p['❌']['name']}  vs  ⭕ {p['⭕']['name']}"
    elif len(p) == 1:
        sym = list(p.keys())[0]
        return f"{sym} {p[sym]['name']} joined\nWaiting for opponent..."
    else:
        return "🎮 XOXO Game\nTap any box to join"


# INLINE QUERY
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="🎮 Start XOXO Game",
        description="2 Player only",
        input_message_content=InputTextMessageContent(
            "🎮 XOXO Game\nTap any box to join"
        ),
        reply_markup=board_markup(["⬜"] * 9)
    )
    await update.inline_query.answer([result], cache_time=0)


# BUTTON HANDLER
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    game_id = query.inline_message_id or query.message.message_id

    if game_id not in games:
        games[game_id] = {
            "board": ["⬜"] * 9,
            "turn": None,
            "players": {},   # "❌"/"⭕" : {id,name}
            "finished": False
        }

    game = games[game_id]

    # GAME FINISHED
    if game["finished"]:
        await query.answer("⛔ Game already finished", show_alert=True)
        return

    # PLAYER JOIN
    if user.id not in [p["id"] for p in game["players"].values()]:
        if len(game["players"]) >= 2:
            await query.answer(
                "🚫 This game is already full (2 players only)",
                show_alert=True
            )
            return

        symbol = "❌" if "❌" not in game["players"] else "⭕"
        game["players"][symbol] = {
            "id": user.id,
            "name": user.first_name
        }

        if len(game["players"]) == 1:
            game["turn"] = symbol

        await query.edit_message_text(
            game_text(game),
            reply_markup=board_markup(game["board"])
        )
        return

    # CHECK TURN
    symbol = None
    for s, p in game["players"].items():
        if p["id"] == user.id:
            symbol = s

    if symbol != game["turn"]:
        await query.answer("⏳ Wait for your turn", show_alert=True)
        return

    idx = int(query.data)
    if game["board"][idx] != "⬜":
        return

    game["board"][idx] = symbol

    # WIN
    if check_win(game["board"]):
        game["finished"] = True
        await query.edit_message_text(
            f"🏆 {game['players'][symbol]['name']} wins!\n\n"
            f"❌ {game['players']['❌']['name']}  vs  ⭕ {game['players']['⭕']['name']}",
            reply_markup=board_markup(game["board"])
        )
        return

    # DRAW
    if "⬜" not in game["board"]:
        game["finished"] = True
        await query.edit_message_text(
            f"🤝 Match Draw!\n\n"
            f"❌ {game['players']['❌']['name']}  vs  ⭕ {game['players']['⭕']['name']}",
            reply_markup=board_markup(game["board"])
        )
        return

    # NEXT TURN
    game["turn"] = "⭕" if game["turn"] == "❌" else "❌"

    await query.edit_message_text(
        game_text(game),
        reply_markup=board_markup(game["board"])
    )


# START BOT
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(InlineQueryHandler(inline_query))
app.add_handler(CallbackQueryHandler(button))

print("✅ XOXO Inline Bot (Locked Players & One-Time Game) Running...")
app.run_polling()
