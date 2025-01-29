from aiogram.filters.state import StateFilter
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from model import *
# Регистрация Клиента

class Registration(StatesGroup): # Состояние
    name_input = State()
    city_input = State()
    street_input = State()
    house_number_input = State()
    number_input = State()

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
    await state.update_data(name=new_user.name)
    await message.answer(text="Введите Город!")
    await state.set_state(Registration.city_input)

@router.message(Registration.name_input)
async def invalid_name_input(message: Message, state: FSMContext):
    await message.answer(text="Имя должно начинаться с заглавной буквы и состоять только из русских символов!")

@router.message(Registration.city_input, F.text.regexp(r'^[А-Я][а-я]+$'))
async def city_input(message: Message, state: FSMContext):
    data = await state.get_data()
    address = {'city': message.text.lower()}
    if 'address' in data:
        address.update(data['address'])
    else:
        address.update({'street': '', 'house_number': ''})
    await state.update_data(address=address)
    await message.answer(text="Введите Улицу!")
    await state.set_state(Registration.street_input)

@router.message(Registration.city_input)
async def invalid_city_input(message: Message, state: FSMContext):
    await message.answer(text="Город неправильный! Должен начинаться с Заглавной буквы! \n"
                              "Пример: Москва")

@router.message(Registration.street_input, F.text.regexp(r'^[А-Я][а-я]+$'))
async def street_input(message: Message, state: FSMContext):
    data = await state.get_data()
    data['address']['street'] = message.text.lower()
    await state.update_data(address=data['address'])
    await message.answer(text="Введите Номер дома!")
    await state.set_state(Registration.house_number_input)

@router.message(Registration.street_input)
async def invalid_street_input(message: Message, state: FSMContext):
    await message.answer(text="Улица неправильная! Должна начинаться с Заглавной буквы! \n"
                              "Пример: Тверская")

@router.message(Registration.house_number_input, F.text.regexp(r'^[1-9][0-9]*$'))
async def house_number_input(message: Message, state: FSMContext):
    data = await state.get_data()
    data['address']['house_number'] = message.text.lower()
    await state.update_data(address=data['address'])
    await message.answer(text="Введите Номер телефона!")
    await state.set_state(Registration.number_input)

@router.message(Registration.house_number_input)
async def invalid_house_number_input(message: Message, state: FSMContext):
    await message.answer(text="Номер дома неправильный! Он должен включать только Цифры!")

@router.message(Registration.number_input, F.text.regexp(r'^\+7[0-9]{10}$'))
async def number_input(message: Message, state: FSMContext):
    data = await state.get_data()
    data['number'] = message.text
    await state.update_data(number=data['number'])
    await message.answer(text="Регистрация завершена!")

@router.message(Registration.number_input)
async def invalid_number_input(message: Message, state: FSMContext):
    await message.answer(text="Номер неправильный! Пример: +79000000000")