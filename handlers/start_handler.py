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
    if not db.user_info(message.from_user.id):
        db.add_user(message.from_user.id)

    if message.text[7:] == "":
        await message.answer(
            "<b>Приветствуем тебя, в SpamShark!</b> 🦈\n\n"
            "👨🏻‍🏫 Наш сервис может спарсить участников открытых чатов и каналов, а также ты"
            "можешь воспользоваться нашим платным сервисом "
            "<a href='https://t.me/sharkspambot?start=spamcreate'><b>быстрой спам-рассылки</b></a> 📩\n\n"
            'Новостной канал: <b>t.me/spamshark</b>\n'
            "Поддержка: <b>t.me/gojukai_san</b>\n\n"
            '<i>Чтобы начать пользоваться ботом, нажми кнопку <b>"Меню"</b></i>',
            reply_markup=ReplyKeyboardRemove(),
            disable_web_page_preview=True
        )
        await state.clear()
    elif message.text[7:] == "spamcreate":
        await message.answer(
            "🌚 Выберите целевую аудиторию.",
            reply_markup=choose_theme()
        )
