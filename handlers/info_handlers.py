from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.info_buttons import main_info_buttons, rating_buttons, \
    how_to_increase_button, back_from_stats
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
            f"🟩 Спамер (от <code>100</code> 🏆):\n"
            f"└ <code>6</code>% от пополнений рефералов\n\n"
            f"🟪 Мейкер (от <code>500</code> 🏆):\n"
            f"├ <code>9</code>% от пополнений рефералов\n"
            f"└ -<code>0.2</code>₽ за <code>1</code> сообщение при спам-рассылке\n\n"
            f"🟧 Легенда (от <code>1000</code> 🏆):\n"
            f"├ <code>12</code>% от пополнений рефералов\n"
            f"├ -<code>0.4</code>₽ за <code>1</code> сообщение при спам-рассылке\n"
            f"└ Ты. Легенда.\n\n"
            f"👨🏻‍🏫 Подробнее о том, как повысить рейтинг, Ты можешь узнать нажав по кнопке ниже",
            reply_markup=rating_buttons()
        )

    elif thing == "stats":
        await call.message.edit_text(
            "⚔️ <b>ТОП-10 по рейтингу</b>\n\n",
            reply_markup=back_from_stats()
        )

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
            "- За каждый заказ спам-рассылки, Ты получаешь +<code>1</code>🏆!\n\n"
            "2️⃣ <b>Способ</b>\n"
            "- Приглашай друзей по своей реферальной ссылке и получай +<code>10</code>🏆!\n"
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
        f"🟩 Спамер (от <code>100</code> 🏆):\n"
        f"└ <code>6</code>% от пополнений рефералов\n\n"
        f"🟪 Мейкер (от <code>500</code> 🏆):\n"
        f"├ <code>9</code>% от пополнений рефералов\n"
        f"└ -<code>0.2</code>₽ за <code>1</code> сообщение при спам-рассылке\n\n"
        f"🟧 Легенда (от <code>1000</code> 🏆):\n"
        f"├ <code>12</code>% от пополнений рефералов\n"
        f"├ -<code>0.3</code>₽ за <code>1</code> сообщение при спам-рассылке\n"
        f"└ Ты. Легенда.\n\n"
        f"👨🏻‍🏫 Подробнее о том, как повысить рейтинг, Ты можешь узнать нажав по кнопке ниже",
        reply_markup=rating_buttons()
    )
