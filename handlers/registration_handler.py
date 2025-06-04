from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# from model import ClientTable  # раскомментируйте при наличии моделей

router = Router()

class Registration(StatesGroup):
    name_input = State()
    city_input = State()
    street_input = State()
    house_number_input = State()
    number_input = State()
    done = State()

@router.message(Command("register"))
async def register(message: Message, state: FSMContext):
    await message.answer("Введите Имя (на русском, с заглавной буквы):")
    await state.set_state(Registration.name_input)

@router.message(Registration.name_input, F.text.regexp(r'^[А-ЯЁ][а-яё]+$'))
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите город (с заглавной буквы):")
    await state.set_state(Registration.city_input)

@router.message(Registration.name_input)
async def invalid_name(message: Message, state: FSMContext):
    await message.answer("❌ Имя должно начинаться с заглавной буквы и содержать только русские буквы.")

@router.message(Registration.city_input, F.text.regexp(r'^[А-ЯЁ][а-яё\s-]+$'))
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Введите улицу (с заглавной буквы):")
    await state.set_state(Registration.street_input)

@router.message(Registration.city_input)
async def invalid_city(message: Message, state: FSMContext):
    await message.answer("❌ Город должен начинаться с заглавной буквы и содержать только русские буквы!")

@router.message(Registration.street_input, F.text.regexp(r'^[А-ЯЁ][а-яё0-9\s-]+$'))
async def process_street(message: Message, state: FSMContext):
    await state.update_data(street=message.text)
    await message.answer("Введите номер дома (например: 17, 17А, 5/2Б):")
    await state.set_state(Registration.house_number_input)

@router.message(Registration.street_input)
async def invalid_street(message: Message, state: FSMContext):
    await message.answer("❌ Улица должна начинаться с заглавной буквы и содержать только русские буквы, цифры, пробелы и дефисы!")

@router.message(Registration.house_number_input, F.text.regexp(r'^[0-9]+[а-яА-Я]?(\/[0-9]+[а-яА-Я]?)?$'))
async def process_house_number(message: Message, state: FSMContext):
    await state.update_data(house_number=message.text)
    await message.answer("Введите номер телефона в формате +79000000000:")
    await state.set_state(Registration.number_input)

@router.message(Registration.house_number_input)
async def invalid_house_number(message: Message, state: FSMContext):
    await message.answer("❌ Номер дома должен содержать цифры и необязательно букву или дробь в конце!")

@router.message(Registration.number_input, F.text.regexp(r'^\+79\d{9}$'))
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    user_data = await state.get_data()
    # Здесь должен быть код для сохранения пользователя в БД, например:
    # client = ClientTable.create(user_id=message.from_user.id, **user_data)
    await message.answer("✅ Регистрация завершена! Теперь вы можете пользоваться ботом.")
    await state.clear()

@router.message(Registration.number_input)
async def invalid_phone(message: Message, state: FSMContext):
    await message.answer("❌ Неверный формат номера! Пример: +79000000000")