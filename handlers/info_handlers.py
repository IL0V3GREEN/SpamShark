from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.info_buttons import main_info_buttons, rating_buttons, \
    how_to_increase_button, back_from_stats, review_buttons
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
            f"└ +<code>3</code>% от пополнений рефералов\n\n"
            f"🟪 Мейкер (от <code>500</code> 🏆):\n"
            f"├ +<code>6</code>% от пополнений рефералов\n"
            f"└ -<code>0.5</code>₽ за <code>1</code> сообщение при спам-рассылке\n\n"
            f"🟧 Легенда (от <code>1000</code> 🏆):\n"
            f"├ +<code>9</code>% от пополнений рефералов\n"
            f"├ -<code>1</code>₽ за <code>1</code> сообщение при спам-рассылке\n"
            f"└ Ты. Легенда.\n\n"
            f"👨🏻‍🏫 Подробнее о том, как повысить рейтинг, Ты можешь узнать нажав по кнопке ниже",
            reply_markup=rating_buttons()
        )

    elif thing == "top":
        await call.message.edit_text(
            "⚔️ <b>ТОП-10 по рейтингу</b>\n\n"
            f"{db.top_rating_list()}",
            reply_markup=back_from_stats(db.user_info(call.from_user.id)['username'])
        )

    elif thing == "review":
        await call.message.edit_text(
            "📝 <b>Написать отзыв можно, нажав на кнопку снизу</b>",
            reply_markup=review_buttons()
        )


@router.callback_query(F.data.startswith("topmake"))
async def username_visibility(call: CallbackQuery):
    action = call.data.split("_")[1]
    if action == "invisible":
        db.update_string(call.from_user.id, {'username': 'Скрыт'})
        await call.answer("🙈 Твой ник скрыт из ТОПа")
        await call.message.edit_text(
            "⚔️ <b>ТОП-10 по рейтингу</b>\n\n"
            f"{db.top_rating_list()}",
            reply_markup=back_from_stats(db.user_info(call.from_user.id)['username'])
        )

    elif action == "visible":
        if call.from_user.username is not None:
            username = f"@{call.from_user.username}"
        else:
            username = call.from_user.full_name
        db.update_string(call.from_user.id, {'username': f'{username}'})
        await call.answer("👀 Твой ник виден в ТОПе")
        await call.message.edit_text(
            "⚔️ <b>ТОП-10 по рейтингу</b>\n\n"
            f"{db.top_rating_list()}",
            reply_markup=back_from_stats(db.user_info(call.from_user.id)['username'])
        )


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
        f"└ +<code>3</code>% от пополнений рефералов\n\n"
        f"🟪 Мейкер (от <code>500</code> 🏆):\n"
        f"├ +<code>6</code>% от пополнений рефералов\n"
        f"└ -<code>0.5</code>₽ за <code>1</code> сообщение при спам-рассылке\n\n"
        f"🟧 Легенда (от <code>1000</code> 🏆):\n"
        f"├ +<code>9</code>% от пополнений рефералов\n"
        f"├ -<code>1</code>₽ за <code>1</code> сообщение при спам-рассылке\n"
        f"└ Ты. Легенда.\n\n"
        f"👨🏻‍🏫 Подробнее о том, как повысить рейтинг, Ты можешь узнать нажав по кнопке ниже",
        reply_markup=rating_buttons()
    )
