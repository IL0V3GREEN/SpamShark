from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards.spamCreator_buttons import choose_theme
from mongo import Database


db = Database()
router = Router()


@router.message(Command(commands="start"))
async def start_handle(message: Message, state: FSMContext):
    if message.text[7:] == "":
        await message.answer(
            "Приветствуем тебя в SpamShark!\n\n"
            "👨🏻‍🏫 Наш сервис поможет тебе спарсить участников открытых чатов, а также, ты "
            "можешь воспользоваться нашим платным сервисом быстрой "
            "<a href='https://t.me/spamsharkbot?start=spamcreate'>спам-рассылки</a> 📩\n\n"
            'Новостной канал: <b>@spamshark</b>\n'
            "Поддержка: <b>@rrassvetov</b>\n\n"
            '<i>Чтобы начать пользоваться ботом, нажми кнопку "Меню"</i>',
            reply_markup=ReplyKeyboardRemove(),
            disable_web_page_preview=True
        )
    elif message.text[7:] == "spamcreate":
        await message.answer(
            "🌚 Выберите целевую аудиторию.",
            reply_markup=choose_theme()
        )

    await state.clear()
