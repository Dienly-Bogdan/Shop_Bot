from aiogram.filters.state import StateFilter
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from model import *

# Регистрация Клиента
# Продажа товара клиенту
# Добавление в корзину клиента
# Вывод Корзины и Список заказов


class Registration(StatesGroup): # Состояние
    name_input = State()
    address_input = State()
    number_input = State()
    buy = State()
    order = State()


router = Router()



@router.message(StateFilter(None), Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer(text="Добро Пожаловать в Компьютерный Магазин ПКРу \n"
                              "Чтобы продолжить, нужно пройти регистрацию! Введите команду /register",)

@router.message(StateFilter(None), Command('register'))
async def register(message: Message, state: FSMContext):
    await message.answer(text="Введите Имя!")
    await state.set_state(Registration.name_input)

@router.message(Registration.name_input, F.text.regexp(r'^[А-Я][а-я]+$'))
async def name_input(message: Message, state: FSMContext):
    new_user = Client()
    new_user.name = message.text.lower()
    await state.update_data(name=new_user)
    await message.answer(text="Введите Адрес! (Город, Улица, Номер Дома) \n"
                              "Пример: Москва, Тверская, 17")
    await state.set_state(Registration.address_input)

@router.message(Registration.name_input)
async def name_input(message: Message, state: FSMContext):
    await message.answer(text="Имя должно начинаться с заглавной буквы и состоять только из русских символов!")


@router.message(Registration.address_input, F.text.regexp(r'([А-Яа-яЁё\-\s]+),\s*([А-Яа-яЁё\-\s]+),\s*(\d+)'))
async def address_input(message: Message, state: FSMContext):
    address = message.text.lower()
    await state.update_data(address=address)

    await message.answer(text="Введите Номер телефона!")

    await state.set_state(Registration.number_input)

@router.message(Registration.address_input)
async def address_input(message: Message, state: FSMContext):
    await message.answer(text="Адрес неправильный! Пример: Москва, Тверская, 17")


@router.message(Registration.number_input, F.text.regexp(r'^[7][9][0-9]+$'))
async def number_input(message: Message, state: FSMContext):
    number = message.text.lower()
    await state.update_data(number=number)

    await message.answer(text="Введите Номер телефона!")


@router.message(Registration.number_input)
async def number_input(message: Message, state: FSMContext):
    await message.answer(text="Номер неправильный! Пример: +790000000")

