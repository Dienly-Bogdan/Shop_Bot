from aiogram.filters.state import StateFilter
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from model import *
from handlers import registration_handler
from keyboards import *

# Добавление в корзину клиента
# Вывод Корзины и Список заказов
# Продажа товара клиенту

router = Router()


class Order(StatesGroup): # Состояние
    basket = State() # Корзина
    ready = State() # Готовые
    build = State() # Сборка
    periphery = State() # Переферия


@router.message(StateFilter(None), Command("buy"))
async def buy(message: Message, state: FSMContext):
    await message.answer(text="Что вас интересует? \n"
                              "Готовые ПК \n"
                              "Сборка ПК \n"
                              "Подбор Комплектующих \n")
    # Будет выводиться клавиатура

@router.message(StateFilter(None), Command("gotovie"))
async def gotovie(message: Message, state: FSMContext):
    ... # Будут выдаваться все модели компьютеров готовые в наличии
    await state.set_state(Order.ready)
    # Запрос и вывод всех пк

@router.message(StateFilter(None), Command("sborka"))
async def sborka(message: Message, state: FSMContext):
    ... # подбор комплектующих для сборки
    await state.set_state(Order.build)
    # Запрос и вывод всех пк


@router.message(StateFilter(None), Command("periphery"))
async def periphery(message: Message, state: FSMContext):
    ... # Перефирия
    await state.set_state(Order.periphery)
    # Запрос и вывод всей перефирии

