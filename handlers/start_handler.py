from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from mongo import Database


db = Database()
router = Router()


@router.message(Command(commands="start"))
async def start_handle(message: Message, state: FSMContext):
    if not db.user_info(message.from_user.id):
        db.add_user(message.from_user.id)
    await message.answer(
        "<b>Приветствуем тебя, в SpamShark!</b> 🦈\n\n"
        "👨🏻‍🏫 У нас ты сможешь спарсить участников открытых чатов и каналов, а также "
        "сможешь воспользоваться нашим платным сервисом <b>быстрой спам-рассылки</b> 📩\n\n"
        'Новостной канал: <b>t.me/spamshark</b>\n'
        "Поддержка: <b>t.me/gojukai_san</b>\n\n"
        '<i>Чтобы начать пользоваться ботом, нажми кнопку <b>"Меню"</b></i>',
        reply_markup=ReplyKeyboardRemove(),
        disable_web_page_preview=True
    )
    await state.clear()
