from pyrogram import Client
from aiogram.filters import Command
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os
import asyncio
import random
from keyboards.where_pars_buttons import where_spamming


class ParseStates(StatesGroup):
    chat_username = State()
    channel_username = State()


router = Router()


@router.message(Command(commands="parse"))
async def start_parsing(message: Message):
    await message.answer(
        "🌚 Каких пользователей парсим?",
        reply_markup=where_spamming()
    )


@router.callback_query(F.data.startswith("parsetype"))
async def getting_spam_locate(call: CallbackQuery, state: FSMContext):
    locate = call.data.split("_")[1]
    if locate == "chat":
        await call.message.edit_text(
            "✏️ Введите юзернейм открытой группы (чата)\n\n"
            "<b>пример: alphaspam1</b>"
        )
        await state.set_state(ParseStates.chat_username)

    else:
        await call.message.edit_text(
            "✏️ Введите юзернейм открытого канала с комментариями\n\n"
            "<b>пример: alphaspam3</b>"
        )
        await state.set_state(ParseStates.channel_username)


@router.message(ParseStates.chat_username, F.text)
async def getting_username(message: Message, state: FSMContext, bot: Bot):
    username = message.text
    app = Client('botik1')
    if "@" not in username and "https" not in username:
        if os.path.exists(f"{username}.txt"):
            os.remove(f"{username}.txt")

        animation_count = 0
        await message.answer(
            "♨️ Подготовка...\n\n"
            f"{animation_count}%"
        )
        file = open(f"{username}.txt", "w+")
        async with app:
            async for member in app.get_chat_members(username):
                if not member.user.is_bot and member.user.username is not None:
                    file.write(f"{member.user.username}\n")

            while animation_count <= 90:
                animation_count += random.randint(6, 9)
                await bot.edit_message_text(
                    f"🩻\n\n"
                    f"{animation_count}%",
                    message.chat.id,
                    message.message_id + 1
                )
                await asyncio.sleep(2)

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
            "📛 Введите username (пример: alphaspam1) чата без @ и https://, как в примере"
        )
