from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from states import OrderSteps
from aiogram.fsm.context import FSMContext

async def main_menu():
    build = ReplyKeyboardBuilder()
    build.row(
        types.KeyboardButton(text="Сделать заказ")
    )
    return build.as_markup(resize_keyboard=True)


def color_menu():
    bild = ReplyKeyboardBuilder()
    bild.row(
        types.KeyboardButton(text="🌹Розы🌹"),
        types.KeyboardButton(text="🌷Тюльпаны🌷"),
    )
    bild.row(
        types.KeyboardButton(text="🌼Ромашки🌼"),
        types.KeyboardButton(text="🌸Эустомы🌸")
    )

    return bild.as_markup(resize_keyboard=True)



async def show_flowers(message: types.Message, flowers_db, vid, state: FSMContext):
    flowers = await flowers_db.get_products_by_category(vid)

    if not flowers:
        await message.answer("К сожалению, таких цветов сейчас нет в наличии.")
        return

    kb = ReplyKeyboardBuilder()
    for name, price, image_path in flowers:
        photo = types.FSInputFile(image_path)

        await message.answer_photo(photo=photo, caption=f"🌹 {name}\n💰 Цена: {price} руб.")

        kb.row(types.KeyboardButton(text=f"{name}"))
    kb.row(types.KeyboardButton(text="⬅️ Назад"))
    await state.set_state(OrderSteps.choosing_flower)
    await message.answer("Выберите, какой цветок хотите заказать:",
                         reply_markup=kb.as_markup(resize_keyboard=True))

