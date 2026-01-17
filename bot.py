# bot.py
import json
from typing import Any, Dict

import telebot
from telebot import types

from config import BOT_TOKEN
from database.data_manager import DataManager
from keyboards.main_keyboards import create_main_keyboard
from keyboards.inline_keyboards import (
    create_categories_keyboard,
    create_product_detail_keyboard,
    build_sets_keyboard,
    build_category_products_keyboard,
)

# ====================== Инициализация ======================
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
data_manager = DataManager()
user_states: Dict[int, Dict[str, Any]] = {}

print("Бот магазина музыкальных инструментов запущен!")

# ====================== Константы ======================
CATEGORY_NAMES = {
    "guitars": "🎸 Гитары",
    "keyboards": "🎹 Клавишные",
    "drums": "🥁 Ударные",
    "winds": "🎷 Духовые",
    "accessories": "🎧 Аксессуары",
}

WELCOME_TEXT = """<b>Добро пожаловать в MusicShop Bot!</b>

Я помогу:
• подобрать музыкальный инструмент
• посмотреть цены и наличие
• собрать готовый набор
• сохранить понравившиеся товары ❤️

Выберите действие в меню ниже."""

HELP_TEXT = """<b>Доступные команды:</b>

/start — главное меню
/help — справка
/favorites — избранные товары

<b>Как пользоваться:</b>
1) Откройте «Каталог инструментов» и выберите категорию
2) Откройте карточку товара и нажмите «Оформить заказ» или «В избранное»
"""

ORDER_TEXT = """<b>Оформление заказа</b>

Чтобы оформить заказ, отправьте одним сообщением:
1) <b>Название товара</b>
2) <b>Ваш телефон</b>
3) <b>Город</b> (или удобный способ доставки)

Пример:
<i>Yamaha F310, +7 777 123 45 67, Алматы</i>

Менеджер свяжется с вами для подтверждения."""

# ====================== Основные функции ======================
def send_product_info(chat_id: int, product: dict, product_id: str, is_random: bool = False) -> None:
    """Отправляет информацию о товаре"""
    prefix = "🎲 <b>Случайная рекомендация:</b>\n\n" if is_random else ""

    text = (
        f"{prefix}<b>{product['name']}</b>\n\n"
        f"{product['description']}\n\n"
        f"{product['address']}\n"
        f"{product.get('work_time', '')}\n"
        f"Цена: <b>{product.get('price', '—')}</b>"
    )

    bot.send_message(
        chat_id,
        text,
        reply_markup=create_product_detail_keyboard(product_id),
    )


def show_favorites(message: types.Message) -> None:
    """Показывает избранные товары пользователя"""
    favorites = data_manager.db.get_favorites(message.from_user.id)

    if not favorites:
        bot.reply_to(message, "Ваше избранное пусто ❤️\nДобавляйте товары из каталога.")
        return

    text = "<b>Ваши избранные товары:</b>\n\n"
    for fav in favorites:
        price = fav.get("price") or "—"
        text += f"❤️ <b>{fav['name']}</b> — {price}\n{fav['address']}\n\n"

    bot.send_message(message.chat.id, text, reply_markup=create_main_keyboard())


# ====================== Команды ======================
@bot.message_handler(commands=["start"])
def cmd_start(message: types.Message) -> None:
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=create_main_keyboard())


@bot.message_handler(commands=["help"])
def cmd_help(message: types.Message) -> None:
    bot.send_message(message.chat.id, HELP_TEXT, reply_markup=create_main_keyboard())


@bot.message_handler(commands=["favorites", "избранное"])
def cmd_favorites(message: types.Message) -> None:
    show_favorites(message)


# ====================== Обработчик КНОПОК главного меню ======================
@bot.message_handler(content_types=["text"])
def handle_main_menu_buttons(message: types.Message) -> None:
    text = message.text.strip()

    if text == "🎸 Каталог инструментов":
        show_categories(message)

    elif text == "🎁 Готовые наборы":
        show_sets(message)

    elif text == "🎲 Случайный товар":
        show_random_product(message)

    elif text in ["❤️ Избранное", "Избранное ❤️", "Избранное"]:
        show_favorites(message)

    elif text == "ℹ️ Помощь":
        cmd_help(message)

    elif text == "↩️ Главное меню":
        cmd_start(message)

    else:
        bot.send_message(
            message.chat.id,
            "Не понял команду 😅\nИспользуйте кнопки меню.",
            reply_markup=create_main_keyboard(),
        )


# ====================== WebApp данные ======================
@bot.message_handler(content_types=["web_app_data"])
def handle_webapp_data(message):
    """Если используете WebApp-витрину, она может отправлять данные сюда."""
    chat_id = message.chat.id
    try:
        data = json.loads(message.web_app_data.data)

        if data.get("action") == "toggle_favorite":
            product_id = int(data["attraction_id"])
            if data_manager.db.is_favorite(chat_id, product_id):
                data_manager.db.remove_favorite(chat_id, product_id)
                bot.send_message(chat_id, "Убрано из ❤️ избранного")
            else:
                data_manager.db.add_favorite(chat_id, product_id)
                name = data_manager.get_attraction(product_id)["name"]
                bot.send_message(chat_id, f"Добавлено в ❤️ избранное!\n<b>{name}</b>")
            return

        if data.get("action") == "open_route":
            set_id = int(data["route_id"])
            show_set_info(chat_id, set_id)
            return

        if data.get("action") == "open_attraction":
            product_id = int(data["attraction_id"])
            product = data_manager.get_attraction(product_id)
            if product:
                send_product_info(chat_id, product, str(product_id))
            else:
                bot.send_message(chat_id, "Товар не найден")
            return

    except Exception as e:
        print(f"Ошибка WebApp: {e}")
        bot.send_message(chat_id, "Ошибка при обработке данных из витрины")


# ====================== Вспомогательные функции ======================
def show_categories(message: types.Message) -> None:
    bot.send_message(
        message.chat.id,
        "Выберите категорию товаров:",
        reply_markup=create_categories_keyboard(),
    )


def show_random_product(message: types.Message) -> None:
    product = data_manager.get_random_attraction()
    if not product:
        bot.send_message(message.chat.id, "Товары не найдены")
        return

    send_product_info(message.chat.id, product, str(product["id"]), is_random=True)


def show_sets(message: types.Message) -> None:
    sets_ = data_manager.get_all_routes()
    if not sets_:
        bot.send_message(message.chat.id, "Наборы ещё не добавлены")
        return

    markup = build_sets_keyboard(sets_)
    bot.send_message(
        message.chat.id,
        "Выберите готовый набор:",
        reply_markup=markup,
    )


def show_products_by_category(chat_id: int, category: str) -> None:
    products = data_manager.get_attractions_by_category(category)

    if not products:
        bot.send_message(chat_id, "В этой категории пока пусто")
        return

    category_name = CATEGORY_NAMES.get(category, category)
    markup = build_category_products_keyboard(products)

    bot.send_message(chat_id, f"<b>{category_name}</b>:", reply_markup=markup)


def show_set_info(chat_id: int, set_id: int) -> None:
    set_ = data_manager.get_route(set_id)
    if not set_:
        bot.send_message(chat_id, "Набор не найден")
        return

    products = data_manager.get_route_attractions(set_id)
    points = "\n".join(f"• {p['name']}" for p in products) or "—"

    text = (
        f"<b>{set_['name']}</b>\n\n"
        f"{set_['description']}\n\n"
        f"<b>Состав набора:</b>\n{points}\n\n"
        f"Нажмите «Каталог инструментов», чтобы открыть карточки товаров."
    )

    bot.send_message(chat_id, text, reply_markup=create_main_keyboard())


# ====================== Inline callbacks ======================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: types.CallbackQuery) -> None:
    data = call.data
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    try:
        if data.startswith("cat_"):
            category = data.split("_", 1)[1]
            show_products_by_category(chat_id, category)

        elif data.startswith("product_"):
            product_id = int(data.split("_", 1)[1])
            product = data_manager.get_attraction(product_id)
            if product:
                user_states[user_id] = {"last_product": str(product_id)}
                send_product_info(chat_id, product, str(product_id))

        elif data == "random_product":
            product = data_manager.get_random_attraction()
            if product:
                user_states[user_id] = {"last_product": str(product["id"])}
                send_product_info(chat_id, product, str(product["id"]), is_random=True)

        elif data.startswith("set_"):
            set_id = int(data.split("_", 1)[1])
            show_set_info(chat_id, set_id)

        elif data.startswith("order_"):
            product_id = int(data.split("_", 1)[1])
            product = data_manager.get_attraction(product_id)
            if product:
                bot.send_message(chat_id, f"Вы выбрали: <b>{product['name']}</b>\n\n{ORDER_TEXT}")
            else:
                bot.send_message(chat_id, ORDER_TEXT)

        elif data.startswith("fav_"):
            product_id = int(data.split("_", 1)[1])
            if data_manager.db.is_favorite(user_id, product_id):
                data_manager.db.remove_favorite(user_id, product_id)
                bot.answer_callback_query(call.id, "Убрано из избранного")
            else:
                data_manager.db.add_favorite(user_id, product_id)
                bot.answer_callback_query(call.id, "Добавлено в избранное ❤️")

        elif data == "back_to_categories":
            show_categories(call.message)

        elif data == "back_to_main":
            bot.delete_message(chat_id, call.message.message_id)
            cmd_start(call.message)

    except Exception as exc:
        print(f"Ошибка в callback: {exc}")
        bot.answer_callback_query(call.id, "Произошла ошибка", show_alert=True)


# ====================== Запуск ======================
if __name__ == "__main__":
    if BOT_TOKEN == "8599629156:AAHkWBgInDYLIoGGQzC3LfD9YLhjbqlDcDQ":
        print("❗ Укажите токен бота в переменной окружения BOT_TOKEN или в config.py")
    bot.infinity_polling()
