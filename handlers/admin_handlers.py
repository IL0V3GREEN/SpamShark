from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.adm_buttons import main_menu
from mongo import Database


db = Database()
router = Router()


@router.message(Command(commands="adm"))
async def admin_panel(message: Message):
    await message.answer("👨🏻‍💻 <b>Админ панель</b>", reply_markup=main_menu(db.get_shop_status()))


@router.callback_query(F.data.startswith("admpanel"))
async def change_shop_status(call: CallbackQuery):
    db.change_shop_status()
    await call.message.edit_text("👨🏻‍💻 <b>Админ панель</b>", reply_markup=main_menu(db.get_shop_status()))

