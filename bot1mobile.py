from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

#Токен бота
from config import TOKEN

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Илюха, привет!')


def main():
    """Запуск бота"""
    application = Application.builder().token(TOKEN).build()

    #Обработчик команд
    application.add_handler(CommandHandler("start", start))

    application.run_polling()


if __name__ == '__main__':
    main()