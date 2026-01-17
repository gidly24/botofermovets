from telebot import types


WEBAPP_URL = "https://gidly24.github.io/music-shop/"  # ← замените на свой GitHub Pages


def create_main_keyboard():
    """Главная клавиатура меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn1 = types.KeyboardButton("🎸 Каталог инструментов")
    btn2 = types.KeyboardButton("🎁 Готовые наборы")
    btn3 = types.KeyboardButton("🎲 Случайный товар")
    btn4 = types.KeyboardButton("❤️ Избранное")
    btn5 = types.KeyboardButton("ℹ️ Помощь")

    # WebApp витрина (по желанию можно убрать)
    web_app_button = types.KeyboardButton(
        "🛒 Витрина",
        web_app=types.WebAppInfo(url=WEBAPP_URL),
    )

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(web_app_button)
    markup.add(btn5)

    return markup


def create_back_button():
    """Кнопка возврата в главное меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("↩️ Главное меню")
    markup.add(button)
    return markup
