import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)
from models import SessionLocal, Question, UserQuizSession

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# Active quiz sessions
ACTIVE = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Welcome to BPSC Quiz Bot!\n/start_quiz to begin.")

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    session = SessionLocal()

    questions = session.query(Question).order_by(Question.id).limit(10).all()
    ACTIVE[user_id] = {"index": 0, "score": 0, "questions": questions}

    await send_question(update, context, user_id)

async def send_question(update, context, user_id):
    data = ACTIVE[user_id]
    q = data["questions"][data["index"]]

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"ans|{i}")]
        for i, opt in enumerate([q.option1, q.option2, q.option3, q.option4])
    ]

    await context.bot.send_message(
        chat_id=user_id,
        text=f"Q{data['index']+1}: {q.question}",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    choice = int(query.data.split("|")[1])
    data = ACTIVE[user_id]
    q = data["questions"][data["index"]]

    if choice == q.correct_option:
        data["score"] += 1
        reply = "✅ Correct!"
    else:
        reply = "❌ Wrong!"

    await query.edit_message_text(reply)

    data["index"] += 1
    if data["index"] >= len(data["questions"]):
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🎉 Quiz Over!\nYour score: {data['score']}/10",
        )
        del ACTIVE[user_id]
        return

    await send_question(update, context, user_id)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("start_quiz", start_quiz))
    app.add_handler(CallbackQueryHandler(check_answer))

    app.run_polling()

if __name__ == "__main__":
    main()
