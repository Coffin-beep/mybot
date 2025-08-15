from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

#Токен бота
TOKEN = '7727573588:AAHnvceU5d2BHf507280XX7XYtKhzSbuymk'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Илюха, привет!')

def main():
    """Запуск бота"""
    updater = Updater(TOKEN)

    #Обработчик команд
    dispatcher = updater.dispatcher

    #Обработчик команд
    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()