from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="/register")
    builder.button(text="/buy")
    builder.button(text="/my_orders")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_product_types_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Готовые ПК")
    builder.button(text="Сборка ПК")
    builder.button(text="Периферия")
    builder.button(text="Отмена")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Отмена")
    return builder.as_markup(resize_keyboard=True)

def get_products_keyboard(products: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for product in products:
        builder.add(InlineKeyboardButton(
            text=f"{product.name} - {product.price} руб.",
            callback_data=f"product_{product.id}"
        ))
    builder.adjust(1)
    return builder.as_markup()

def get_quantity_keyboard(product_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.add(InlineKeyboardButton(
            text=str(i),
            callback_data=f"quantity_{product_id}_{i}"
        ))
    builder.add(InlineKeyboardButton(
        text="Отмена",
        callback_data="cancel"
    ))
    builder.adjust(3, 3, 1)
    return builder.as_markup()

def get_cart_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Оформить заказ",
        callback_data="checkout"
    ))
    builder.add(InlineKeyboardButton(
        text="Продолжить покупки",
        callback_data="continue"
    ))
    builder.add(InlineKeyboardButton(
        text="Очистить корзину",
        callback_data="clear_cart"
    ))
    builder.adjust(1)
    return builder.as_markup()