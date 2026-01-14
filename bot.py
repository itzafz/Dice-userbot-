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


# INLINE QUERY
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="🎮 Start XOXO Game",
        description="2 Player inline Tic Tac Toe",
        input_message_content=InputTextMessageContent(
            "🎮 **XOXO Game Started**\nTap any box to join!",
            parse_mode="Markdown"
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
            "turn": "❌",
            "players": {}  # user_id : symbol
        }

    game = games[game_id]

    # PLAYER JOIN LOGIC
    if user.id not in game["players"]:
        if len(game["players"]) >= 2:
            await query.answer("🚫 Game full! You are spectator.", show_alert=True)
            return
        symbol = "❌" if "❌" not in game["players"].values() else "⭕"
        game["players"][user.id] = symbol

    # CHECK TURN
    if game["players"][user.id] != game["turn"]:
        await query.answer("⏳ Wait for your turn!", show_alert=True)
        return

    idx = int(query.data)

    if game["board"][idx] != "⬜":
        return

    game["board"][idx] = game["turn"]

    player_name = user.first_name

    # WIN
    if check_win(game["board"]):
        await query.edit_message_text(
            f"🏆 **{player_name} ({game['turn']}) wins!**",
            reply_markup=board_markup(game["board"]),
            parse_mode="Markdown"
        )
        games.pop(game_id, None)
        return

    # DRAW
    if "⬜" not in game["board"]:
        await query.edit_message_text(
            "🤝 **Match Draw!**",
            reply_markup=board_markup(game["board"]),
            parse_mode="Markdown"
        )
        games.pop(game_id, None)
        return

    # SWITCH TURN
    game["turn"] = "⭕" if game["turn"] == "❌" else "❌"

    next_player_id = [uid for uid, s in game["players"].items() if s == game["turn"]]
    next_name = "Next Player"
    if next_player_id:
        next_name = context.bot.get_chat_member(
            query.message.chat.id, next_player_id[0]
        ).user.first_name if query.message else "Player"

    await query.edit_message_reply_markup(
        reply_markup=board_markup(game["board"])
    )


# START APP
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(InlineQueryHandler(inline_query))
app.add_handler(CallbackQueryHandler(button))

print("✅ XOXO Inline Bot with Player Lock Running...")
app.run_polling()
