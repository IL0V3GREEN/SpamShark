from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.spamCreator_buttons import choose_theme
from mongo import Database
from keyboards.support_button import support_link


db = Database()
router = Router()


@router.message(Command(commands="start"))
async def start_handle(message: Message, state: FSMContext):
    if message.text[7:] == "":
        await message.answer(
            "<b>Приветствуем тебя в SpamShark!</b>\n\n"
            "👨🏻‍🏫 Наш сервис поможет тебе спарсить участников открытых чатов, а также, ты "
            "можешь воспользоваться нашим платным сервисом быстрой "
            "<a href='https://t.me/spamsharkbot?start=spamcreate'><b>спам-рассылки</b></a> 📩\n\n"
            '<i>Чтобы начать пользоваться ботом, нажми кнопку <b>"Меню"</b></i>',
            reply_markup=support_link()
        )
    elif message.text[7:] == "spamcreate":
        await message.answer(
            "🌚 Выберите целевую аудиторию.",
            reply_markup=choose_theme()
        )

    await state.clear()
