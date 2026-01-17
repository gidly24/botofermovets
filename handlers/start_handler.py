from telebot import types
from database.data_manager import DataManager
from keyboards.main_keyboards import create_main_keyboard


def setup_start_handlers(bot, data_manager: DataManager):
    @bot.message_handler(commands=["start"])
    def send_welcome(message: types.Message):
        welcome_text = (
            "🎵 Добро пожаловать в MusicShop Bot!\n"
            "Здесь вы можете выбрать инструмент, посмотреть наличие и цены,\n"
            "а также собрать готовый набор."
        )
        bot.send_message(message.chat.id, welcome_text, reply_markup=create_main_keyboard())

    @bot.message_handler(commands=["help"])
    def send_help(message: types.Message):
        help_text = (
            "ℹ️ Команды:\n"
            "/start — главное меню\n"
            "/help — справка\n"
            "/favorites — избранные товары"
        )
        bot.send_message(message.chat.id, help_text)
