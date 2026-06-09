# 💐 Flower Shop Bot

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Aiogram](https://img.shields.io/badge/aiogram-3.x-blue?logo=telegram)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite)

Telegram-бот для онлайн-магазина цветов. Позволяет выбрать букет из каталога, оформить заказ и автоматически уведомляет администратора.

---

## 🌹 Возможности

- Просмотр каталога по категориям (розы, тюльпаны, ромашки, эустомы)
- Фото и цена каждого товара прямо в чате
- Пошаговое оформление заказа через FSM
- Выбор упаковки, адрес доставки, подтверждение
- Уведомление администратора о новом заказе
- Редактирование данных перед подтверждением

---

## 🛠 Стек

| Область | Инструменты |
|---|---|
| Bot Framework | Aiogram 3, asyncio |
| База данных | SQLite3 |
| Конфиг | python-dotenv |

---

## 📁 Структура проекта

```
flower-shop-bot/
├── main.py              # Точка входа, запуск бота
├── handlers.py          # Обработчики сообщений
├── keyboards.py         # Клавиатуры и меню
├── states.py            # FSM-состояния заказа
├── SQL.py               # Класс работы с базой данных
├── flowers_data.db      # SQLite база
├── .env                 # Токен и ID администратора
├── requirements.txt
└── README.md
```

---

## ⚙️ Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/ВАШ_NICKNAME/flower-shop-bot.git
cd flower-shop-bot
```

### 2. Создайте виртуальное окружение

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Создайте файл `.env`

```env
TOKEN=ваш_токен_от_BotFather
ADMIN_ID=ваш_telegram_id
```

### 5. Создайте таблицу в базе данных

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    category TEXT NOT NULL
);
```

### 6. Запустите бота

```bash
python main.py
```

---

## 🔄 Сценарий заказа

```
Старт → Выбор категории → Выбор цветка → Количество
→ Упаковка → Адрес → Имя → Телефон → Подтверждение → ✅
```
