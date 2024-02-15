from pathlib import Path
import sys
import os
import django
current_directory = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(current_directory))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
import environ
from app.models import Student
from asgiref.sync import sync_to_async

logging.basicConfig( 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

PHONE, EMAIL, LEVEL, MOTIVATION = range(4)

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
        f"Thank you for your email!\n\nNow click /english_level to choose your level of English."
        )
    
    return ConversationHandler.END
    
async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_phone_set(update, context):
        return
    
    user_id = update.message.from_user.id
    user = await sync_to_async(Student.objects.get)(external_id=user_id)    

    email = user.email
    
    if email == "":
        email = "(not set)"

    level = user.english_level
    if level == "":
        level = "(not set)"

    motivation = user.bio
    if motivation == "":
        motivation = "(not set)"

    await update.message.reply_text(
        f"""
Here is the information we got from you:

Your unique id: {user.external_id}
Phone number: {user.phone_number}
Your email: {email}
Your language level: {level}
Motivationa letter: {motivation}
        """
    )

async def english_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_phone_set(update, context):
        return ConversationHandler.END
    
    reply_keyboard = [["A1", "A2", "B1", "B2", "C1"]]

    await update.message.reply_text(
        "What's your English level?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Your English level?"
        ),
    )

    return LEVEL

async def level_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text
    user_id = update.message.from_user.id

    user = await sync_to_async(Student.objects.get)(external_id=user_id)
    user.english_level=user_answer
    await sync_to_async(Student.save)(user)

    await update.message.reply_text(
        "That's great! Tell us why do you want to learn language abroad?"
    )

    return MOTIVATION

async def why_abroad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    motivation = update.message.text
    user_id = update.message.from_user.id

    user = await sync_to_async(Student.objects.get)(external_id=user_id)
    user.bio=motivation
    await sync_to_async(Student.save)(user)

    await update.message.reply_text(
        """
Amazing! You are registered, we will contact you soon!
        
Press /me to check the information you provided :)
        """
    )

    return ConversationHandler.END


async def ensure_phone_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user = await sync_to_async(Student.objects.get)(external_id=user_id)

    if user.phone_number is None:
        await update.message.reply_text(
            "Please, complete the registration by providing your phone number first."
        )
        return False
    
    return True

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Alright, I hope to see you soon.",
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
    english_handler = ConversationHandler(
        entry_points=[CommandHandler('english_level', english_level)],
        states={
            LEVEL: [MessageHandler(filters.Regex("^(A1|A2|B1|B2|C1)$") & ~filters.COMMAND, level_set)],
            MOTIVATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, why_abroad)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    me_handler = CommandHandler('me', me)
    

    application.add_handler(start_handler)
    application.add_handler(conv_handler)
    application.add_handler(me_handler)
    application.add_handler(english_handler)

    application.run_polling()


if __name__ == '__main__':
    main()