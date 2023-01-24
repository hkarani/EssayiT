from typing import Dict

import telegram
from telegram import Update
from telegram.ext import CallbackContext

from tgbot.models import User

def get_user_text_message(update: Update, context: CallbackContext):
    text = update.effective_message.text
    return text
    
    

def handle_text(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    message = "You sent a text"
    context.bot.send_message(
        chat_id=u.user_id,
        text=message,
    )

