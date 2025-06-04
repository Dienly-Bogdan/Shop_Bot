from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from model import Client
from database import ClientTable, Database
from keyboards import get_main_keyboard
import re

class Registration(StatesGroup):
    name_input = State()
    city_input = State()
    street_input = State()
    house_number_input = State()
    number_input = State()

router = Router()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer(
        "Добро пожаловать в Компьютерный Магазин ПКРу!\n"
        "Чтобы продолжить, нужно пройти регистрацию! Введите команду /register",
        reply_markup=get_main_keyboard()
    )

@router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    # Check if user already registered
    client = ClientTable.get_by_phone(str(message.from_user.id))
    if client:
        await message.answer(
            "Вы уже зарегистрированы!\n"
            "Можете перейти к покупкам с помощью /buy",
            reply_markup=get_main_keyboard()
        )
        return
        
    await message.answer(
        "Начнём регистрацию!\n"
        "Введите ваше имя (только русские буквы, начинается с заглавной):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Registration.name_input)

@router.message(Registration.name_input, F.text.regexp(r'^[А-Я][а-я]+\s*[А-Я]*[а-я]*$'))
async def name_input(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш город:")
    await state.set_state(Registration.city_input)

@router.message(Registration.name_input)
async def invalid_name_input(message: Message):
    await message.answer("❌ Имя должно начинаться с заглавной буквы и состоять только из русских символов!")

@router.message(Registration.city_input, F.text.regexp(r'^[А-Я][а-я]+$'))
async def city_input(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Введите вашу улицу:")
    await state.set_state(Registration.street_input)

@router.message(Registration.city_input)
async def invalid_city_input(message: Message):
    await message.answer("❌ Город должен начинаться с заглавной буквы и содержать только русские буквы!")

@router.message(Registration.street_input, F.text.regexp(r'^[А-Я][а-я]+\s*[А-Я]*[а-я]*$'))
async def street_input(message: Message, state: FSMContext):
    await state.update_data(street=message.text)
    await message.answer("Введите номер дома:")
    await state.set_state(Registration.house_number_input)

@router.message(Registration.street_input)
async def invalid_street_input(message: Message):
    await message.answer("❌ Улица должна начинаться с заглавной буквы и содержать только русские буквы!")

@router.message(Registration.house_number_input, F.text.regexp(r'^[1-9][0-9]*[а-яА-Я]?$'))
async def house_number_input(message: Message, state: FSMContext):
    await state.update_data(house_number=message.text)
    await message.answer("Введите номер телефона в формате +79000000000:")
    await state.set_state(Registration.number_input)

@router.message(Registration.house_number_input)
async def invalid_house_number_input(message: Message):
    await message.answer("❌ Номер дома должен содержать цифры и необязательно букву в конце!")

@router.message(Registration.number_input, F.text.regexp(r'^\+7[0-9]{10}$'))
async def number_input(message: Message, state: FSMContext):
    data = await state.get_data()
    
    # Create client object
    client = Client()
    client.name = data.get('name', '')
    client.address = f"{data.get('city', '')}, {data.get('street', '')}, {data.get('house_number', '')}"
    client.number = message.text
    
    # Save to database
    client_id = ClientTable.add(client)
    
    await message.answer(
        "✅ Регистрация успешно завершена!\n"
        f"Ваш ID: {client_id}\n"
        "Теперь вы можете делать покупки с помощью команды /buy",
        reply_markup=get_main_keyboard()
    )
    await state.clear()

@router.message(Registration.number_input)
async def invalid_number_input(message: Message):
    await message.answer("❌ Неверный формат номера! Пример: +79000000000")