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
import telegram
import telegram.ext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
import environ
from app.models import Student, Country
from asgiref.sync import sync_to_async

logging.basicConfig( 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

PHONE, EMAIL, WRONG_NUMBER = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    await sync_to_async(Student.objects.get_or_create)(
        external_id=user_id, 
        first_name=first_name, 
        last_name=last_name
        )
    
    await update.message.reply_text(
        f"Hello, {first_name}! Nice to see you here!\n\nPlease, tap /set_phone to start the registration for an amazing language program!"
        )
    
async def set_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please, type your phone number below.\n\nSend /cancel to stop the registration."
        )
    
    return PHONE
    
async def phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number: str = update.message.text

    try:
        number_int = int(phone_number)
    except ValueError:
        await update.message.reply_text(
        f"Invalid number, please use this format: 000000000 "
        )
        return PHONE
    
    user_id = update.message.from_user.id
    
    student = await sync_to_async(Student.objects.get)(external_id=user_id)
    student.phone_number = number_int
    await sync_to_async(Student.save)(student)

    # # convert function save to asynchronous
    # converted_fun = sync_to_async(student.save)
    # # call converted function with no arguments
    # await converted_fun()

    await update.message.reply_text(
        f"Thank you! What's your email?"
        )
    return EMAIL
    
async def email(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    email = update.message.text

    user_id = update.message.from_user.id
    student = await sync_to_async(Student.objects.get)(external_id=user_id)
    student.email = email
    await sync_to_async(Student.save)(student)
    
    await update.message.reply_text(
        f"Thank you! Tell us, what is your English level?"
        )
    
async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    me_information = await sync_to_async(lambda:(Student.objects.filter)(external_id=user_id).values("phone_number", "email", "external_id").first())()
    

    if me_information:
        phone_number = me_information["phone_number"]
        email = me_information["email"]
        personal_id = me_information["external_id"] 
        
        if email == "":
            email = "(not set)"

        await update.message.reply_text(
            f"Here is the information we got from you:\n\nYour unique id: {personal_id}\n\nPhone number: {phone_number}\n\nYour email: {email}"
        )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.",
    )

    return ConversationHandler.END

DIRECTORY = Path(__file__).resolve().parent.parent.parent.parent

def main() -> None:
    env = environ.Env(
        BOT_TOKEN=(str, '')
    )
    environ.Env.read_env(DIRECTORY / ".env")

    application = ApplicationBuilder().token(env("BOT_TOKEN")).build()

    start_handler = CommandHandler('start', start)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("set_phone", set_phone)],
        states={
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_number)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    me_handler = CommandHandler('me', me)

    application.add_handler(start_handler)
    application.add_handler(conv_handler)
    application.add_handler(me_handler)

    application.run_polling()


if __name__ == '__main__':
    main()