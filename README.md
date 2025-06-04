# Телеграм-бот для компьютерного магазина "ПКРу"

Этот телеграм-бот позволяет пользователям:
- Регистрироваться в системе
- Просматривать товары различных категорий
- Формировать заказы
- Управлять корзиной покупок
- Просматривать историю заказов

## Особенности проекта
- Полностью асинхронная архитектура
- Интеграция с MySQL базой данных
- Валидация вводимых данных
- Интерактивные клавиатуры
- Состояния для управления процессом покупки
- Корзина товаров с временным хранилищем

## Технологический стек
- Python 3.11+
- aiogram 3.x (асинхронный фреймворк для Telegram ботов)
- MySQL (база данных)
- mysql-connector-python (драйвер для работы с MySQL)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/Dienly-Bogdan/Shop_Bot.git
cd shop_bot
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка базы данных
1. Установите MySQL сервер
2. Создайте базу данных:
```sql
CREATE DATABASE computer_shop;
```
3. Создайте таблицы:
```sql
USE computer_shop;

CREATE TABLE Client (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    number VARCHAR(20) NOT NULL
);

CREATE TABLE Product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    guarantee INT
);

CREATE TABLE `Order` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_client INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
    FOREIGN KEY (id_client) REFERENCES Client(id)
);

CREATE TABLE OrderItem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `Order`(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);
```

### 4. Настройка конфигурации
Создайте файл `config.py` в корне проекта со следующим содержимым:
```python
# Конфигурация приложения
TOKEN = "ВАШ_ТОКЕН_БОТА"

# Конфигурация базы данных
base = {
    "host": "localhost",
    "user": "ВАШ_ПОЛЬЗОВАТЕЛЬ_БД",
    "password": "ВАШ_ПАРОЛЬ_БД",
    "database": "computer_shop"
}
```

### 5. Запуск бота
```bash
python main.py
```

## Использование бота

### Основные команды
- `/start` - Начало работы с ботом
- `/register` - Регистрация нового пользователя
- `/buy` - Начать покупки
- `/my_orders` - Просмотр истории заказов
- `/cart` - Просмотр корзины

### Процесс регистрации
1. Пользователь вводит `/register`
2. Бот запрашивает:
   - Имя (на русском, с заглавной буквы)
   - Город
   - Улицу
   - Номер дома
   - Номер телефона (в формате +79000000000)
3. После успешной регистрации пользователь получает уведомление

### Процесс покупки
1. Пользователь вводит `/buy`
2. Выбор категории товаров:
   - Готовые ПК
   - Сборка ПК
   - Периферия
3. Просмотр товаров в выбранной категории
4. Выбор количества товара
5. Добавление товара в корзину
6. Управление корзиной:
   - Оформить заказ
   - Продолжить покупки
   - Очистить корзину

### Просмотр заказов
- Команда `/my_orders` показывает историю заказов пользователя с:
  - Номером заказа
  - Датой оформления
  - Суммой заказа
  - Статусом заказа

## Структура проекта
```
computer_shop_bot/
├── config.py.example      # Пример конфигурационного файла
├── database.py            # Работа с базой данных
├── handler.py             # Основной обработчик (устаревший)
├── handlers/
│   ├── order_handler.py   # Обработчик заказов
│   └── registration_handler.py # Обработчик регистрации
├── keyboards.py           # Генерация клавиатур
├── main.py                # Точка входа
├── model.py               # Модели данных
├── README.md              # Этот файл
└── requirements.txt       # Зависимости
```

## Настройка для разработки
1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `config.py` на основе `config.py.example`

4. Запустите бота:
```bash
python main.py
```

## Возможности для расширения
1. Добавление админ-панели для управления товарами
2. Интеграция платежной системы
3. Система скидок и промокодов
4. Отслеживание статуса заказа
5. Система отзывов и рейтингов

