import telegram
from telegram import Bot
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters,  ConversationHandler, CallbackContext, Updater, ContextTypes
import os
import dotenv
from dotenv import load_dotenv
import random
import string

# Replace with your Telegram Bot API token
load_dotenv()
api_key = os.getenv("API_KEY")
TOKEN: Final = api_key
BOT_USERNAME: Final = '@otpverifierBot'

# Create a dictionary to store OTPs for users
otp_dict = {}

# Define conversation states
OTP_STATE = 1

# Generate a random OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# Start command handler
#def start(update: Update, context: CallbackContext):
def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    otp = generate_otp()
    otp_dict[user_id] = otp
    update.message.reply_text(f'Your OTP is: {otp}')
    update.message.reply_text('Send your OTP to verify.')

# Verify OTP handler
#def verify_otp(update: Update, context: CallbackContext):
def verify_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_input = update.message.text.strip()

    if user_id in otp_dict and user_input == otp_dict[user_id]:
        update.message.reply_text('OTP verified successfully!')
    else:
        update.message.reply_text('OTP verification failed. Please try again.')

""" def main(token, bot, updater):
     bot = Bot(token=TOKEN)
     updater = Updater(bot=bot)
     dispatcher = Updater.dispatcher """

""" def main(update, context):
    bot = Bot(token=TOKEN)
    updater = Updater(bot=bot)
    #updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher """
def main(Update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={OTP_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_otp)]},
        fallbacks=[]
    )

    """ dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle() """

""" if __name__ == '__main__':
    main() """


if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('otp', verify_otp))

    #messages
    app.add_handler(MessageHandler(filters.TEXT, main))

    print("Polling...")
    app.run_polling(poll_interval=3)