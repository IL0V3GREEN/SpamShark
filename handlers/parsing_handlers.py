from pyrogram import Client
from aiogram.filters import Command
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from mongo import Database
import os
from keyboards.parse_buttons import where_parsing


class ParseStates(StatesGroup):
    chat_username = State()
    channel_username = State()


db = Database()
router = Router()


@router.message(Command(commands="parse"))
async def start_parsing(message: Message, state: FSMContext):
    await message.answer(
        "🌚 Каких пользователей парсим?",
        reply_markup=where_parsing()
    )
    await state.clear()


@router.callback_query(F.data.startswith("parsetype"))
async def getting_spam_locate(call: CallbackQuery, state: FSMContext):
    locate = call.data.split("_")[1]
    if locate == "chat":
        await call.message.edit_text(
            "✏️ Введи юзернейм открытой группы (чата):\n\n"
            "<i>пример: alphaspam1</i>"
        )
        await state.set_state(ParseStates.chat_username)
    else:
        await call.message.edit_text(
            "✏️ Введи юзернейм открытого канала с комментариями:\n\n"
            "<i>пример: alphaspam3</i>"
        )
        await state.set_state(ParseStates.channel_username)


@router.message(ParseStates.chat_username, F.text)
async def getting_username(message: Message, state: FSMContext, bot: Bot):
    username = message.text
    app = Client('parse', 23474509, "087d8368b34304fa5a4510dbdb6dcdcb")
    if "@" not in username and "https" not in username and "t.me/" not in username:
        if os.path.exists(f"{username}.txt"):
            os.remove(f"{username}.txt")

        file = open(f"{username}.txt", "w+")
        async with app:
            async for member in app.get_chat_members(username):
                if not member.user.is_bot and member.user.username is not None and member.user.last_online_date:
                    file.write(f"{member.user.username}\n")

            await message.answer("⏳ Wait 30 seconds..")
            await bot.delete_message(message.chat.id, message.message_id + 1)

            file.close()
            doc_txt = FSInputFile(f"{username}.txt")
            count = await app.get_chat_members_count(username)
            await message.answer_document(
                doc_txt,
                caption=f"🕵🏻‍♀️ <b>@{username}</b>\n\n"
                        f"Количество участников: <b>{count}</b>"
            )
            await state.clear()

    else:
        await message.answer(
            "📛 Введи username (пример: alphaspam1) чата без @ и https://, как в примере."
        )
