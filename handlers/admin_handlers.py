import asyncio
import os
import random
import requests
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.adm_buttons import main_menu, adm_back_from_stats, tg_sets, back_to_account_manager, proxy_buttons
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from mongo import Database
from pyrogram import Client


db = Database()
router = Router()


class SendingMessage(StatesGroup):
    message_to_all = State()


class TgSettings(StatesGroup):
    saving_session = State()
    getting_api = State()
    get_code = State()
    new_proxy = State()


@router.message(Command(commands="adm"))
async def admin_panel(message: Message):
    if message.from_user.id == 6364771832:
        await message.answer(
            "👨🏻‍💻 <b>Админ панель</b>\n\n"
            "  - Смена статуса шопа\n"
            "  - Общая статистика",
            reply_markup=main_menu(db.get_shop_status())
        )


@router.callback_query(F.data.startswith("admpanel"))
async def change_shop_status(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")[1]
    if action == "statuschange":
        db.change_shop_status()
        await call.message.edit_text(
            "👨🏻‍💻 <b>Админ панель</b>\n\n"
            "  - Смена статуса шопа\n"
            "  - Общая статистика",
            reply_markup=main_menu(db.get_shop_status())
        )
    elif action == "stats":
        await call.message.edit_text(
            "<b>📊 Статистика</b>\n\n"
            f'💶 <b>Профит "грязный"</b>\n'
            f"├ <b>За сегодня</b>: <code>{db.earned_today()}</code>₽\n"
            f"├ <b>За 7 дней</b>: <code>{db.earned_week()}</code>₽\n"
            f"├ <b>За 30 дней</b>: <code>{db.earned_month()}</code>₽\n"
            f"└ <b>Всего</b>: <code>{db.earned_alltime()}</code>₽\n\n"
            f"🕵🏻‍♀️ <b>Пользователи</b>\n"
            f"├ <b>За сегодня</b>: <code>{db.users_joined_today()}</code>\n"
            f"├ <b>За 7 дней</b>: <code>{db.users_joined_week()}</code>\n"
            f"├ <b>За 30 дней</b>: <code>{db.users_joined_month()}</code>\n"
            f"└ <b>Всего</b>: <code>{len(list(db.collection.find()))}</code>\n\n",
            reply_markup=adm_back_from_stats()
        )
    elif action == "message":
        await call.message.edit_text("Введи текст рассылки:", reply_markup=adm_back_from_stats())
        await state.set_state(SendingMessage.message_to_all)

    # elif action == "accounts":
    #     await call.message.edit_text(
    #         "📱 <b>Менеджер аккаунтов</b>\n\n"
    #         "<b>Телеграм акки</b>\n"
    #         f"├ <b>Валидных:</b> <code>{await Sessions.valid_sessions()}</code>\n"
    #         f"├ <b>Спамблок:</b> <code>{await Sessions.spammers_sessions()}</code>\n"
    #         f"└ <b>Всего:</b> <code>{await Sessions.valid_sessions() + await Sessions.spammers_sessions()}</code>",
    #         reply_markup=tg_sets()
    #     )

    elif action == 'proxy':
        await call.message.edit_text(
            f"🌐 <b>Менеджер прокси</b>\n\n"
            f"<b>Текущее прокси</b>\n"
            f"├ <b>scheme:</b> <code>{db.current_proxy()['scheme']}</code>\n"
            f"├ <b>hostname:</b> <code>{db.current_proxy()['hostname']}</code>\n"
            f"├ <b>port:</b> <code>{db.current_proxy()['port']}</code>\n"
            f"├ <b>username:</b> <code>{db.current_proxy()['username']}</code>\n"
            f"└ <b>password:</b> <code>{db.current_proxy()['password']}</code>",
            reply_markup=proxy_buttons()
        )


@router.callback_query(F.data == "proxy_add")
async def proxy_list(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "📨 Отправь мне прокси в таком формате -> scheme:hostname:port:username:password"
    )
    await state.set_state(TgSettings.new_proxy)


@router.message(TgSettings.new_proxy, F.text)
async def getting_proxy(message: Message, state: FSMContext, bot: Bot):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    proxy = message.text.split(":")
    db.update_proxy(proxy[0], proxy[1], int(proxy[2]), proxy[3], proxy[4])
    await message.answer(
        f"🌐 <b>Менеджер прокси</b>\n\n"
        f"<b>Текущее прокси</b>\n"
        f"├ <b>scheme:</b> <code>{db.current_proxy()['scheme']}</code>\n"
        f"├ <b>hostname:</b> <code>{db.current_proxy()['hostname']}</code>\n"
        f"├ <b>port:</b> <code>{db.current_proxy()['port']}</code>\n"
        f"├ <b>username:</b> <code>{db.current_proxy()['username']}</code>\n"
        f"└ <b>password:</b> <code>{db.current_proxy()['password']}</code>\n\n"
        f"⚠️ <i>Не забудь, что теперь нужно входить в аккаунты с этого прокси</i>",
        reply_markup=proxy_buttons()
    )
    await state.clear()


# @router.callback_query(F.data.startswith("tgsets"))
# async def sessions_manipulations(call: CallbackQuery, state: FSMContext):
#     action = call.data.split("_")[1]
#     if action == 'add':
#         await call.message.edit_text(
#             "Отправь мне файл с LOLZ (Pyrogram .session):",
#             reply_markup=back_to_account_manager()
#         )
#         await state.set_state(TgSettings.saving_session)
#
#     elif action == "check":
#         await call.message.edit_text(
#             "📱 <b>Менеджер аккаунтов</b>\n\n"
#             "<b>Телеграм акки</b>\n"
#             f"├ <b>Валидных:</b> <code>{await Sessions.valid_sessions()}</code>\n"
#             f"├ <b>Спамблок:</b> <code>{await Sessions.spammers_sessions()}</code>\n"
#             f"└ <b>Всего:</b> <code>{await Sessions.valid_sessions() + await Sessions.spammers_sessions()}</code>\n\n"
#             "🕵🏻‍♀️ <i>Чекап аккаунтов завершен</i>",
#             reply_markup=tg_sets()
#         )
#
#
# @router.message(TgSettings.saving_session, F.document)
# async def getting_session(message: Message, bot: Bot, state: FSMContext):
#     await bot.delete_message(message.chat.id, message.message_id - 1)
#     file_id = message.document.file_id
#     file = await bot.get_file(file_id)
#     name = f"user_{random.randint(0, 9999)}.session"
#     path = os.path.join('sessions', name)
#     await bot.download_file(file.file_path, destination=path)
#     await state.update_data(saving_session=name)
#     await state.set_state(TgSettings.getting_api)
#     await message.answer(
#         "Отправь мне api_id & api_hash & phone через * без пробелов:"
#     )
#
#
# @router.message(TgSettings.getting_api, F.text)
# async def getting_apis(message: Message, bot: Bot, state: FSMContext):
#     await bot.delete_message(message.chat.id, message.message_id - 1)
#     try:
#         api_id = int(message.text.split("*")[0])
#         api_hash = message.text.split("*")[1]
#         phone = message.text.split("*")[2]
#         await state.update_data(getting_api=f'{api_id}*{api_hash}')
#         data = await state.get_data()
#         app = Client(
#             str(data['saving_session']).split('.')[0],
#             api_id,
#             api_hash,
#             proxy=db.current_proxy()
#         )
#         await app.connect()
#         phone = await app.send_code(phone)
#         await state.update_data(get_code=phone.phone_code_hash)
#         await message.answer("✉️ Отправь код от Telegram")
#         await state.set_state(TgSettings.get_code)
#
#     except TypeError:
#         await message.answer("📛 Отправь корректный api_id*api_hash*phone")
#
#
# @router.message(TgSettings.get_code, F.text)
# async def auth_profile(message: Message, state: FSMContext, bot: Bot):
#     await bot.delete_message(message.chat.id, message.message_id - 1)
#     data = await state.get_data()
#     app = Client(
#         str(data['saving_session']).split('.')[0],
#         int(str(data['getting_api']).split("*")[0]),
#         str(data['getting_api']).split("*")[1]
#     )
#     await app.sign_in(str(data['getting_api']).split("*")[3], data['get_code'], message.text)
#     await message.answer(
#         "📱 <b>Менеджер аккаунтов</b>\n\n"
#         "<b>Телеграм акки</b>\n"
#         f"├ <b>Валидных:</b> <code>{await Sessions.valid_sessions()}</code>\n"
#         f"├ <b>Спамблок:</b> <code>{await Sessions.spammers_sessions()}</code>\n"
#         f"└ <b>Всего:</b> <code>{await Sessions.valid_sessions() + await Sessions.spammers_sessions()}</code>"
#     )
#
#
# @router.callback_query(F.data == "toAccManager")
# async def back_to_acc_manager(call: CallbackQuery, state: FSMContext):
#     await call.message.edit_text(
#         "📱 <b>Менеджер аккаунтов</b>\n\n"
#         "<b>Телеграм акки</b>\n"
#         f"├ <b>Валидных:</b> <code>{await Sessions.valid_sessions()}</code>\n"
#         f"├ <b>Спамблок:</b> <code>{await Sessions.spammers_sessions()}</code>\n"
#         f"└ <b>Всего:</b> <code>{await Sessions.valid_sessions() + await Sessions.spammers_sessions()}</code>",
#         reply_markup=tg_sets()
#     )
#     await state.clear()


@router.callback_query(F.data == "admback")
async def back_from_adm_stats(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "👨🏻‍💻 <b>Админ панель</b>\n\n"
        "  - Смена статуса шопа\n"
        "  - Общая статистика",
        reply_markup=main_menu(db.get_shop_status())
    )
    await state.clear()


@router.message(SendingMessage.message_to_all, F.text)
async def messaging_to_all(message: Message, state: FSMContext):
    user_lists = list(db.collection.find())
    for user in user_lists:
        params = {
            'chat_id': user['user_id'],
            'text': message.text
        }
        resp = requests.post(
            "https://api.telegram.org/bot6249367873:AAFra-Kvtu6i1V9lS8kvx_9J8-XGxDTxCI8/sendMessage",
            params
        )
        print(resp)
        await asyncio.sleep(0.1)

    await message.answer(
        "👨🏻‍💻 <b>Админ панель</b>\n\n"
        "  - Смена статуса шопа\n"
        "  - Общая статистика",
        reply_markup=main_menu(db.get_shop_status())
    )
    await state.clear()
