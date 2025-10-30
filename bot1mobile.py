from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ConversationHandler,
)
import time
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN1 = os.getenv('TOKEN_BOT_1')
MY_ID_CHAT = os.getenv('MY_ID_CHAT')

print(f"TOKEN loaded: {'YES' if TOKEN1 else 'NO'}")
print(f"MY_ID_CHAT loaded: {'YES' if MY_ID_CHAT else 'NO'}")
print(f"MY_ID_CHAT value: {MY_ID_CHAT}")

TOKEN = TOKEN1
ADMIN_ID_CHAT = MY_ID_CHAT
WAITING_FOR_SUGGESTION = 1

user_cooldowns = {}

async def start(update: Update, context: CallbackContext) -> None:
    print(f"Start command from user: {update.message.from_user.username} (ID: {update.message.from_user.id})")
    await update.message.reply_text(
        'Добро пожаловать в канал с предложениями от CF GROUP!\n'
        'Здесь вы можете написать свои идеи для доработки канала.\n\n'
        'Просто отправьте ваше предложение в этом чате.\n'
        'Обратите внимание: можно отправлять не чаще 1 предложения в 10 минут.',
        reply_markup=ReplyKeyboardRemove()
    )

async def handle_suggestion(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    current_time = time.time()
    
    print(f"Received suggestion from user: {user.username} (ID: {user.id})")
    print(f"Message text: {update.message.text}")

    # Проверка кд
    if user.id in user_cooldowns:
        last_message_time = user_cooldowns[user.id]
        if current_time - last_message_time < 600:  # 10 минут в секундах
            remaining_time = int(600 - (current_time - last_message_time))
            await update.message.reply_text(
                f'Вы можете отправить следующее предложение только через {remaining_time} секунд.'
            )
            return ConversationHandler.END
    
    # Обновляем время последнего сообщения
    user_cooldowns[user.id] = current_time

    # Пересылаем предложение админу
    try:
        print(f"Attempting to send message to admin chat: {ADMIN_ID_CHAT}")
        forwarded_msg = await context.bot.send_message(
            chat_id=ADMIN_ID_CHAT,
            text=f"Новое предложение от @{user.username or 'N/A'} (ID: {user.id}):\n\n{update.message.text}"
        )
        print(f"✅ Message successfully sent to admin. Message ID: {forwarded_msg.message_id}")
    except Exception as e:
        print(f"❌ Error sending message to admin: {e}")
        await update.message.reply_text(
            '❌ Произошла ошибка при отправке предложения. Попробуйте позже.'
        )
        return ConversationHandler.END

    await update.message.reply_text(
        '✅ Ваше предложение отправлено на модерацию! Спасибо за вашу активность.'
    )

    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        'Отправка предложения отменена.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    """Запуск бота"""
    print("Starting bot...")
    
    if not TOKEN:
        print("❌ ERROR: TOKEN not loaded!")
        return
        
    if not ADMIN_ID_CHAT:
        print("❌ ERROR: ADMIN_ID_CHAT not loaded!")
        return
    
    application = Application.builder().token(TOKEN).build()

    # Обработчик команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))

    # Обработчик текстовых сообщений (для предложений)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_suggestion))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
