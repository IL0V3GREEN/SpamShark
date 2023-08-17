from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.info_buttons import main_info_buttons, rating_buttons, how_to_increase_button
from mongo import Database


db = Database()
router = Router()


@router.message(Command(commands="faq"))
async def start_parsing(message: Message):
    await message.answer(
        "👨🏻‍🏫 <b>Информационная панель</b>",
        reply_markup=main_info_buttons()
    )


@router.callback_query(F.data.startswith("info"))
async def info_handling(call: CallbackQuery):
    thing = call.data.split("_")[1]
    if thing == "rating":
        await call.message.edit_text(
            f"💥 <b>Рейтинговая система</b>\n\n"
            f"<b>Рейтинг:</b> <code>{db.count_rating(call.from_user.id)}</code> 🏆\n\n"
            f"📌 Что дают кубки:\n"
            f"🟩 Спамер (от 100 🏆):\n"
            f"└ +5% от пополнений рефералов\n\n"
            f"🟪 Мейкер (от 500 🏆):\n"
            f"├ +10% от пополнений рефералов\n"
            f"└ -0.25₽ за 1 сообщение при спам-рассылке\n\n"
            f"🟧 Легенда (от 1000 🏆):\n"
            f"├ +15% от пополнений рефералов\n"
            f"├ -0.5₽ за 1 сообщение при спам-рассылке\n"
            f"└ Ты. Легенда.\n\n"
            f"👨🏻‍🏫 Подробнее о том, как повысить рейтинг, Ты можешь узнать нажав по кнопке ниже",
            reply_markup=rating_buttons()
        )

    elif thing == "top":
        pass

    elif thing == "review":
        pass


@router.callback_query(F.data.startswith("rating"))
async def rating_handlers(call: CallbackQuery):
    action = call.data.split("_")[1]
    if action == "increase":
        await call.message.edit_text(
            "🔥 <b>Как повышать рейтинг?</b>\n\n"
            "🧐 На текущий момент, есть два способа:\n"
            "1️⃣ <b>Способ</b>\n"
            "- За каждый заказ спам-рассылки, Ты получаешь +1🏆\n\n"
            "2️⃣ <b>Спосок</b>\n\n"
            "- Ты получаешь +10🏆, если Пользователь авторизуется в боте по твоей реферальной ссылке.\n"
            f"Ссылка: <code>https://t.me/spamsharkbot?start=ref_{call.from_user.id}</code>\n",
            reply_markup=how_to_increase_button()
        )

    else:
        await call.message.edit_text(
            "👨🏻‍🏫 <b>Информационная панель</b>",
            reply_markup=main_info_buttons()
        )


@router.callback_query(F.data == "increaseback")
async def increase_buttons_back(call: CallbackQuery):
    await call.message.edit_text(
        f"💥 <b>Рейтинговая система</b>\n\n"
        f"<b>Рейтинг:</b> <code>{db.count_rating(call.from_user.id)}</code> 🏆\n\n"
        f"📌 Что дают кубки:\n"
        f"🟩 Спамер (от 100 🏆):\n"
        f"└ +5% от пополнений рефералов\n\n"
        f"🟪 Мейкер (от 500 🏆):\n"
        f"├ +10% от пополнений рефералов\n"
        f"└ -0.25₽ за 1 сообщение при спам-рассылке\n\n"
        f"🟧 Легенда (от 1000 🏆):\n"
        f"├ +15% от пополнений рефералов\n"
        f"├ -0.5₽ за 1 сообщение при спам-рассылке\n"
        f"└ Ты. Легенда.\n\n"
        f"👨🏻‍🏫 Подробнее о том, как повысить рейтинг, Ты можешь узнать нажав по кнопке ниже",
        reply_markup=rating_buttons()
    )
