from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

#Токен бота
TOKEN = '7727573588:AAHnvceU5d2BHf507280XX7XYtKhzSbuymk'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Илюха, привет!')

def main():
    """Запуск бота"""
    application = Application.builder().token(TOKEN).build()

    #Обработчик команд
    application.add_handler(CommandHandler("start", start))

    application.start_polling()

    application.idle()

if __name__ == '__main__':
    main()