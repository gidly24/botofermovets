from telebot import types


def create_categories_keyboard():
    """Клавиатура с категориями товаров"""
    markup = types.InlineKeyboardMarkup(row_width=1)

    buttons = [
        types.InlineKeyboardButton("🎸 Гитары", callback_data="cat_guitars"),
        types.InlineKeyboardButton("🎹 Клавишные", callback_data="cat_keyboards"),
        types.InlineKeyboardButton("🥁 Ударные", callback_data="cat_drums"),
        types.InlineKeyboardButton("🎷 Духовые", callback_data="cat_winds"),
        types.InlineKeyboardButton("🎧 Аксессуары", callback_data="cat_accessories"),
    ]
    markup.add(*buttons)
    return markup


def create_product_detail_keyboard(product_id: str):
    """Кнопки под карточкой товара"""
    markup = types.InlineKeyboardMarkup()

    markup.row(
        types.InlineKeyboardButton("🛒 Оформить заказ", callback_data=f"order_{product_id}"),
        types.InlineKeyboardButton("❤️ В избранное", callback_data=f"fav_{product_id}"),
    )
    markup.row(types.InlineKeyboardButton("🎲 Случайный товар", callback_data="random_product"))
    markup.row(types.InlineKeyboardButton("Главное меню", callback_data="back_to_main"))
    return markup


def build_sets_keyboard(sets_):
    """sets_ — список словарей [{'id': 1, 'name': 'Набор ...'}, ...]"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    for s in sets_:
        markup.row(types.InlineKeyboardButton(s["name"], callback_data=f"set_{s['id']}"))
    markup.row(types.InlineKeyboardButton("Главное меню", callback_data="back_to_main"))
    return markup


def build_category_products_keyboard(products):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for p in products:
        markup.row(types.InlineKeyboardButton(p["name"], callback_data=f"product_{p['id']}"))
    markup.row(types.InlineKeyboardButton("Назад к категориям", callback_data="back_to_categories"))
    return markup
