from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards.choosing_theme import choose_theme
from mongo import Database


db = Database()
router = Router()


@router.message(Command(commands="start"))
async def start_handle(message: Message, state: FSMContext):
    if message.text[7:] == "":
        await message.answer(
            "<b>Приветствуем тебя в SpamShark!</b>\n\n"
            "👨🏻‍🏫 Наш сервис может спарсить участников открытых чатов и каналов, а также, ты "
            "можешь воспользоваться нашим платным сервисом быстрой "
            "<a href='https://t.me/spamsharkbot?start=spamcreate'><b>спам-рассылки</b></a> 📩\n\n"
            'Новостной канал: <b>t.me/spamshark</b>\n'
            "Поддержка: <b>t.me/rrassvetov</b>\n\n"
            '<i>Чтобы начать пользоваться ботом, нажми кнопку <b>"Меню"</b></i>',
            reply_markup=ReplyKeyboardRemove(),
            disable_web_page_preview=True
        )
    elif message.text[7:] == "spamcreate":
        await message.answer(
            "🌚 Выберите целевую аудиторию.",
            reply_markup=choose_theme()
        )

    await state.clear()
