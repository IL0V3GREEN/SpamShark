import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.spamCreator_buttons import choose_theme
from mongo import Database


db = Database()
router = Router()


@router.message(Command(commands="start"))
async def start_handle(message: Message, state: FSMContext):
    if not db.user_exists(message.from_user.id):
        if message.text[7:].startswith("ref"):
            ref_id = int(message.text[7:].split("_")[1])
            if ref_id != message.from_user.id:
                db.add_user(message.from_user.id)
                db.update_string(message.from_user.id, {'ref_id': ref_id})
            else:
                await message.answer("Нельзя зарегистрироваться по своей реферальной ссылке!")
        else:
            db.add_user(message.from_user.id)

        await message.answer_sticker("CAACAgIAAxkBAAEKCRxk2__X8I1sEWoCtF30MhfGaPPsVgACJxwAAtqDAAFKAAG1a2gCHgiTMAQ")
        await asyncio.sleep(1)
        await message.answer(
            f"🦈 <b>SpamShark</b>\n\n"
            "📩 Многопоточная <a href='https://t.me/spamsharkbot?start=spamcreate'><b>спам-рассылка</b></a> разошлет "
            "юзерам все, что тебе угодно!\n\n"
            '⚡️ Чтобы начать пользоваться ботом, нажми кнопку <b>"Меню"</b>'
        )

    if message.text[7:] == "":
        await message.answer_sticker("CAACAgIAAxkBAAEKCRxk2__X8I1sEWoCtF30MhfGaPPsVgACJxwAAtqDAAFKAAG1a2gCHgiTMAQ")
        await asyncio.sleep(1)
        await message.answer(
            f"🦈 <b>SpamShark</b>\n\n"
            "📩 Многопоточная <a href='https://t.me/spamsharkbot?start=spamcreate'><b>спам-рассылка</b></a> разошлет "
            "юзерам все, что тебе угодно!\n\n"
            '⚡️ Чтобы начать пользоваться ботом, нажми кнопку <b>"Меню"</b>'
        )
    elif message.text[7:] == "spamcreate":
        await message.answer(
            "🌚 Выберите целевую аудиторию.",
            reply_markup=choose_theme()
        )

    await state.clear()
