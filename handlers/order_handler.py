from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from model import Product, Order
from database import ProductTable, OrderTable, ClientTable
from keyboards import (
    get_product_types_keyboard,
    get_products_keyboard,
    get_quantity_keyboard,
    get_cart_keyboard,
    get_main_keyboard,
    get_cancel_keyboard
)
from typing import Dict, List, Tuple

router = Router()

class OrderState(StatesGroup):
    selecting_category = State()
    selecting_product = State()
    selecting_quantity = State()
    cart = State()
    checkout = State()

# Temporary cart storage {user_id: [(product_id, quantity, price)]}
user_carts: Dict[int, List[Tuple[int, int, float]]] = {}

@router.message(Command("buy"))
async def buy(message: Message, state: FSMContext):
    # Check if user is registered
    client = ClientTable.get_by_phone(str(message.from_user.id))
    if not client:
        await message.answer(
            "❌ Сначала зарегистрируйтесь с помощью команды /register",
            reply_markup=get_main_keyboard()
        )
        return

    await message.answer(
        "Выберите категорию товаров:",
        reply_markup=get_product_types_keyboard()
    )
    await state.set_state(OrderState.selecting_category)

@router.message(OrderState.selecting_category, F.text.in_(["Готовые ПК", "Сборка ПК", "Периферия"]))
async def select_category(message: Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category)
    
    # Get products by category
    products = ProductTable.get_all_products()
    if not products:
        await message.answer("😢 Товары в этой категории временно отсутствуют")
        return
    
    await message.answer(
        f"Товары в категории '{category}':",
        reply_markup=get_products_keyboard(products)
    )
    await state.set_state(OrderState.selecting_product)

@router.message(OrderState.selecting_category, F.text == "Отмена")
async def cancel_category_selection(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Выбор категории отменен",
        reply_markup=get_main_keyboard()
    )

@router.callback_query(OrderState.selecting_product, F.data.startswith("product_"))
async def select_product(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split("_")[1])
    product = ProductTable.get_by_id(product_id)
    
    if not product:
        await callback.answer("Товар не найден")
        return
        
    text = (
        f"🖥️ {product.name}\n"
        f"💰 Цена: {product.price} руб.\n"
        f"📦 В наличии: {product.quantity} шт.\n"
        f"🛡️ Гарантия: {product.guarantee} мес.\n\n"
        "Выберите количество:"
    )
    
    await callback.message.edit_text(text)
    await callback.message.edit_reply_markup(
        reply_markup=get_quantity_keyboard(product_id)
    )
    await state.set_state(OrderState.selecting_quantity)
    await callback.answer()

@router.callback_query(OrderState.selecting_quantity, F.data.startswith("quantity_"))
async def select_quantity(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    product_id = int(parts[1])
    quantity = int(parts[2])
    
    product = ProductTable.get_by_id(product_id)
    if not product:
        await callback.answer("Товар не найден")
        return
        
    if quantity > product.quantity:
        await callback.answer("Недостаточно товара на складе")
        return
        
    # Add to cart
    user_id = callback.from_user.id
    if user_id not in user_carts:
        user_carts[user_id] = []
        
    # Update if already in cart
    found = False
    for i, item in enumerate(user_carts[user_id]):
        if item[0] == product_id:
            user_carts[user_id][i] = (product_id, quantity, product.price)
            found = True
            break
            
    if not found:
        user_carts[user_id].append((product_id, quantity, product.price))
    
    await callback.message.delete()
    await callback.message.answer(
        f"✅ {product.name} x{quantity} добавлен в корзину!",
        reply_markup=get_cart_keyboard()
    )
    await state.set_state(OrderState.cart)
    await callback.answer()

@router.callback_query(OrderState.selecting_quantity, F.data == "cancel")
async def cancel_quantity_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        "Выбор количества отменен",
        reply_markup=get_product_types_keyboard()
    )
    await state.set_state(OrderState.selecting_category)
    await callback.answer()

@router.callback_query(OrderState.cart, F.data == "checkout")
async def checkout(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if user_id not in user_carts or not user_carts[user_id]:
        await callback.answer("Корзина пуста!")
        return
        
    # Get client
    client = ClientTable.get_by_phone(str(user_id))
    if not client:
        await callback.answer("Ошибка: пользователь не найден")
        return
        
    # Prepare data for order
    products = [(item[0], item[1]) for item in user_carts[user_id]]
    
    # Create order
    order_id = OrderTable.create_order(client.id, products)
    
    # Clear cart
    del user_carts[user_id]
    
    await callback.message.answer(
        f"✅ Заказ #{order_id} успешно оформлен!\n"
        "Вы можете посмотреть свои заказы с помощью /my_orders",
        reply_markup=get_main_keyboard()
    )
    await state.clear()
    await callback.answer()

@router.callback_query(OrderState.cart, F.data == "continue")
async def continue_shopping(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите категорию товаров:")
    await callback.message.edit_reply_markup(
        reply_markup=get_product_types_keyboard()
    )
    await state.set_state(OrderState.selecting_category)
    await callback.answer()

@router.callback_query(OrderState.cart, F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if user_id in user_carts:
        del user_carts[user_id]
    
    await callback.message.answer(
        "🛒 Корзина очищена!",
        reply_markup=get_main_keyboard()
    )
    await state.clear()
    await callback.answer()

@router.message(Command("my_orders"))
async def my_orders(message: Message):
    # Get client
    client = ClientTable.get_by_phone(str(message.from_user.id))
    if not client:
        await message.answer(
            "❌ Сначала зарегистрируйтесь с помощью команды /register",
            reply_markup=get_main_keyboard()
        )
        return
        
    orders = OrderTable.get_client_orders(client.id)
    if not orders:
        await message.answer("У вас пока нет заказов")
        return
        
    response = "📦 Ваши заказы:\n\n"
    for order in orders:
        response += (
            f"🔖 Заказ #{order.id}\n"
            f"📅 Дата: {order.date}\n"
            f"💳 Сумма: {order.total_price} руб.\n"
            f"🔄 Статус: {order.status}\n\n"
        )
    
    await message.answer(response)

@router.message(Command("cart"))
async def show_cart(message: Message):
    user_id = message.from_user.id
    if user_id not in user_carts or not user_carts[user_id]:
        await message.answer("🛒 Ваша корзина пуста")
        return
        
    total = 0
    response = "🛒 Ваша корзина:\n\n"
    for item in user_carts[user_id]:
        product_id, quantity, price = item
        product = ProductTable.get_by_id(product_id)
        if product:
            response += f"➖ {product.name} x{quantity} = {price * quantity} руб.\n"
            total += price * quantity
    
    response += f"\n💳 Итого: {total} руб."
    
    await message.answer(
        response,
        reply_markup=get_cart_keyboard()
    )