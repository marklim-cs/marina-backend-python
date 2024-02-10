import asyncio
from pathlib import Path
import sys
import os
import django
current_directory = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(current_directory))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import logging
from telegram import Update
from telegram.ext import filters, Application, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
import environ
from app.models import Student, Country

logging.basicConfig( 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    #Student.objects.create(external_id=user_id, first_name=first_name, last_name=last_name)
    await update.message.reply_text(f"Hello, {first_name}, your id is {user_id}")


DIRECTORY = Path(__file__).resolve().parent.parent.parent.parent

if __name__ == '__main__':
    env = environ.Env(
        BOT_TOKEN=(str, '')
    )
    environ.Env.read_env(DIRECTORY / ".env")

    application = ApplicationBuilder().token(env("BOT_TOKEN")).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()


