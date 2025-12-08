from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # <-- yaha apna token daalo

QUESTIONS = [
    {
        "question": "बिहार की राजधानी क्या है?",
        "options": ["पटना", "गया", "दरभंगा", "मुजफ्फरपुर"],
        "answer": "पटना"
    }
]

user_data = {}

def start(update, context):
    update.message.reply_text("नमस्ते! मैं BPSC Quiz Bot हूँ.\n/startquiz लिखकर क्विज़ शुरू करें।")

def startquiz(update, context):
    question = random.choice(QUESTIONS)
    user_data[update.message.chat_id] = question

    buttons = [[InlineKeyboardButton(opt, callback_data=opt)] for opt in question["options"]]

    update.message.reply_text(question["question"], reply_markup=InlineKeyboardMarkup(buttons))

def check_answer(update, context):
    query = update.callback_query
    user_choice = query.data
    chat_id = query.message.chat_id

    correct = user_data.get(chat_id, {}).get("answer")

    if user_choice == correct:
        query.edit_message_text(f"✔ सही! उत्तर: {correct}")
    else:
        query.edit_message_text(f"❌ गलत! सही उत्तर: {correct}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("startquiz", startquiz))
    dp.add_handler(CallbackQueryHandler(check_answer))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

