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
from datetime import datetime, timedelta

#Токен бота
from config import TOKEN1, MY_ID_CHAT

TOKEN = TOKEN1
ADMIN_ID_CHAT = MY_ID_CHAT
WAITING_FOR_SUGGESTION = 1

user_cooldowns = {}

async def start(update: Update, context: CallbackContext) -> None:
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
        forwarded_msg = await context.bot.send_message(
            chat_id=ADMIN_ID_CHAT,
            text=f"Новое предложение от @{user.username or 'N/A'} (ID: {user.id}):\n\n{update.message.text}"
        )
        print(f"Сообщение отправлено админу. ID сообщения: {forwarded_msg.message_id}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения админу: {e}")
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
    application = Application.builder().token(TOKEN).build()

    # Обработчик команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))

    # Обработчик текстовых сообщений (для предложений)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_suggestion))

    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()
