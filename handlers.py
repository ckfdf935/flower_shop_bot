from os import getenv
from aiogram import Router, F
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from buttons import *
import re
load_dotenv()

ADMIN_ID = getenv('ADMIN_ID')
router = Router()



@router.message(CommandStart())
async def command_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Нажми на кнопку ниже, чтобы оформить заказ.",
        reply_markup=await main_menu()
    )

@router.message(F.text.in_(["Сделать заказ", "Сделать новый заказ"]))
async def start_fsm(message: types.Message, state: FSMContext):
    await state.set_state(OrderSteps.choosing_category)
    await message.answer("Выберите категорию цветов:", reply_markup=color_menu())



@router.message(OrderSteps.choosing_category, (F.text.contains("🌹Розы🌹")) | (F.text.lower() == "розы"))
async def roses_category(message: types.Message, flowers_db, state: FSMContext):
    await show_flowers(message=message, flowers_db=flowers_db, vid="роза", state=state)

@router.message(OrderSteps.choosing_category, (F.text.contains("🌷Тюльпаны🌷")) | (F.text.lower() == "тюльпаны"))
async def tulips_category(message: types.Message, flowers_db, state: FSMContext):
    await show_flowers(message=message, flowers_db=flowers_db, vid="тюльпан", state=state)

@router.message(OrderSteps.choosing_category, (F.text.contains("🌼Ромашки🌼")) | (F.text.lower() == "ромашка"))
async def daisies_category(message: types.Message, flowers_db, state: FSMContext):
    await show_flowers(message=message, flowers_db=flowers_db, vid="ромашка", state=state)

@router.message(OrderSteps.choosing_category, (F.text.contains("🌸Эустомы🌸")) | (F.text.lower() == "эустома"))
async def eustoma_category(message: types.Message, flowers_db, state: FSMContext):
    await show_flowers(message=message, flowers_db=flowers_db, vid="эустома", state=state)



@router.message(OrderSteps.choosing_flower)
async def process_flower_choice(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.set_state(OrderSteps.choosing_category)
        await message.answer("Выберите категорию цветов:", reply_markup=color_menu())
        return

    await state.update_data(chosen_flower=message.text)
    await state.set_state(OrderSteps.waiting_for_quantity)

    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="⬅️ Назад"))

    await message.answer(
        f"Вы выбрали {message.text}. Сколько штук вы хотите заказать?\n(Введите число, например: 5)",
        reply_markup=kb.as_markup(resize_keyboard=True)
    )



@router.message(OrderSteps.waiting_for_quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        # Возвращаемся в самое начало к категориям
        await state.set_state(OrderSteps.choosing_category)
        await message.answer("Выберите категорию цветов заново:", reply_markup=color_menu())
        return

    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите количество цифрами!")
        return

    await state.update_data(quantity=int(message.text))
    await state.set_state(OrderSteps.waiting_for_packaging)

    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="🎀 Лента"), types.KeyboardButton(text="🎁 Крафтовая бумага"))
    kb.row(types.KeyboardButton(text="❌ Без упаковки"))
    kb.row(types.KeyboardButton(text="⬅️ Назад"))

    await message.answer(
        f"Количество ({message.text} шт.) принято! Теперь выберите упаковку:",
        reply_markup=kb.as_markup(resize_keyboard=True)
    )


@router.message(OrderSteps.waiting_for_packaging)
async def process_packaging(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.set_state(OrderSteps.waiting_for_quantity)
        kb = ReplyKeyboardBuilder().row(types.KeyboardButton(text="⬅️ Назад"))
        await message.answer("Введите количество цветов заново:", reply_markup=kb.as_markup(resize_keyboard=True))
        return

    await state.update_data(packaging=message.text)
    await state.set_state(OrderSteps.waiting_for_address)

    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="🏠 Самовывоз"), types.KeyboardButton(text="🚚 Доставка"))
    kb.row(types.KeyboardButton(text="⬅️ Назад"))

    await message.answer("Выберите способ получения заказа:", reply_markup=kb.as_markup(resize_keyboard=True))


@router.message(OrderSteps.waiting_for_address)
async def process_delivery_choice(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.set_state(OrderSteps.waiting_for_packaging)
        kb = ReplyKeyboardBuilder()
        kb.row(types.KeyboardButton(text="🎀 Лента"), types.KeyboardButton(text="🎁 Крафтовая бумага"))
        kb.row(types.KeyboardButton(text="❌ Без упаковки"), types.KeyboardButton(text="⬅️ Назад"))
        await message.answer("Выберите упаковку заново:", reply_markup=kb.as_markup(resize_keyboard=True))
        return

    if message.text == "🏠 Самовывоз":
        await state.update_data(delivery_type="🏠 Самовывоз", address="ул. Ленина")
        await state.set_state(OrderSteps.waiting_for_name)
        kb = ReplyKeyboardBuilder().row(types.KeyboardButton(text="⬅️ Назад"))
        await message.answer("Наш адрес: ул. Ленина \nВведите ваше имя:", reply_markup=kb.as_markup(resize_keyboard=True))

    elif message.text == "🚚 Доставка":
        await state.update_data(delivery_type="🚚 Доставка")
        kb = ReplyKeyboardBuilder().row(types.KeyboardButton(text="⬅️ Назад"))
        await message.answer("Введите ваш адрес доставки:", reply_markup=kb.as_markup(resize_keyboard=True))

    else:

        data = await state.get_data()
        if data.get("delivery_type") == "🚚 Доставка":
            await state.update_data(address=message.text)
            await state.set_state(OrderSteps.waiting_for_name)
            kb = ReplyKeyboardBuilder().row(types.KeyboardButton(text="⬅️ Назад"))
            await message.answer(f"Адрес записан: {message.text}\nВведите ваше имя:", reply_markup=kb.as_markup(resize_keyboard=True))
        else:
            await message.answer("Пожалуйста, используйте кнопки!")


@router.message(OrderSteps.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Назад":
        await state.set_state(OrderSteps.waiting_for_address)
        kb = ReplyKeyboardBuilder()
        kb.row(types.KeyboardButton(text="🏠 Самовывоз"), types.KeyboardButton(text="🚚 Доставка"))
        kb.row(types.KeyboardButton(text="⬅️ Назад"))
        await message.answer("Выберите способ получения заново:", reply_markup=kb.as_markup(resize_keyboard=True))
        return

    await state.update_data(user_name=message.text)
    await state.set_state(OrderSteps.waiting_for_phone)

    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="📱 Отправить номер", request_contact=True))
    kb.row(types.KeyboardButton(text="⬅️ Назад"))

    await message.answer(f"Приятно познакомиться, {message.text}! Введите номер телефона:", reply_markup=kb.as_markup(resize_keyboard=True))


@router.message(OrderSteps.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    # 1. Сначала проверяем текст, но только если он ЕСТЬ (чтобы не было ошибки с контактом)
    if message.text and message.text == "⬅️ Назад":
        await state.set_state(OrderSteps.waiting_for_name)
        await message.answer("Введите ваше имя заново:",
                             reply_markup=ReplyKeyboardBuilder().row(types.KeyboardButton(text="⬅️ Назад")).as_markup(
                                 resize_keyboard=True))
        return

    if message.contact:
        phone = message.contact.phone_number
    elif message.text:
        phone = re.sub(r"\D", "", message.text)
    else:
        await message.answer("Отправьте номер телефона!")
        return

    if len(phone) < 10:
        await message.answer("Номер слишком короткий. Введите корректный номер.")
        return

    await state.update_data(user_phone=phone)
    await state.set_state(OrderSteps.confirm_order)

    data = await state.get_data()
    summary = (
        f"*Ваш заказ:*\n"
        f"🌺 Товар: {data.get('chosen_flower')}\n"
        f"📦 Количество: {data.get('quantity')}\n"
        f"👤 Клиент: {data.get('user_name')}\n"
        f"📱 Тел: {data.get('user_phone')}\n"
        f"📍 Адрес: {data.get('address')}"
    )

    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="✅ Всё верно"))
    kb.row(types.KeyboardButton(text="✏️ Изменить имя"), types.KeyboardButton(text="📞 Изменить номер"))
    await message.answer(summary, reply_markup=kb.as_markup(resize_keyboard=True))


@router.message(OrderSteps.confirm_order)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text == "✅ Всё верно":
        data = await state.get_data()
        admin_summary = f"🔔 **НОВЫЙ ЗАКАЗ**\n\nТовар: {data.get('chosen_flower')}\nИмя: {data.get('user_name')}\nТел: {data.get('user_phone')}"

        try:
            await message.bot.send_message(chat_id=ADMIN_ID, text=admin_summary)

            # Сначала создаем кнопку
            kb = ReplyKeyboardBuilder()
            kb.row(types.KeyboardButton(text='Сделать новый заказ'))

            # Отправляем сообщение об успехе с этой кнопкой
            await message.answer("Спасибо! Заказ передан менеджеру.",
                                 reply_markup=kb.as_markup(resize_keyboard=True))

            # Очищаем состояние в самом конце
            await state.clear()
            return  # Выходим из функции, чтобы код ниже не выполнялся

        except Exception as e:
            print(f"Ошибка: {e}")
            await message.answer("Ошибка отправки админу.")
            return

    elif message.text == "✏️ Изменить имя":
        await state.set_state(OrderSteps.waiting_for_name)
        await message.answer("Введите новое имя:",
                             reply_markup=ReplyKeyboardBuilder().row(types.KeyboardButton(text="⬅️ Назад")).as_markup(
                                 resize_keyboard=True))
        return

    elif message.text == "📞 Изменить номер":
        await state.set_state(OrderSteps.waiting_for_phone)
        kb = ReplyKeyboardBuilder()
        kb.row(types.KeyboardButton(text="📱 Отправить номер", request_contact=True),
               types.KeyboardButton(text="⬅️ Назад"))
        await message.answer("Введите новый номер:", reply_markup=kb.as_markup(resize_keyboard=True))
        return