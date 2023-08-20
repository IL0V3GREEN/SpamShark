from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.adm_buttons import main_menu, adm_back_from_stats
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from mongo import Database


db = Database()
router = Router()


class AdminStates(StatesGroup):
    message_to_all = State()


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
        await call.message.edit_text("Введи текст рассылки:")
        await state.set_state(AdminStates.message_to_all)


@router.callback_query(F.data == "admback")
async def back_from_adm_stats(call: CallbackQuery):
    await call.message.edit_text(
        "👨🏻‍💻 <b>Админ панель</b>\n\n"
        "  - Смена статуса шопа\n"
        "  - Общая статистика",
        reply_markup=main_menu(db.get_shop_status())
    )


@router.callback_query(AdminStates.message_to_all, F.text)
async def messaging_to_all(message: Message, state: FSMContext, bot: Bot):
    user_lists = list(db.collection.find())
    for user in user_lists:
        try:
            await bot.send_message(
                user['user_id'],
                message.text
            )
        except TelegramBadRequest:
            pass
        
    await message.answer(
        "👨🏻‍💻 <b>Админ панель</b>\n\n"
        "  - Смена статуса шопа\n"
        "  - Общая статистика",
        reply_markup=main_menu(db.get_shop_status())
    )
    await state.clear()
