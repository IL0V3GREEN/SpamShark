import asyncio
from LolzteamApi import LolzteamApi
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.spamCreator_buttons import choose_theme
from mongo import Database


db = Database()
router = Router()
lolz = LolzteamApi('01c295d581ca25fd24567b215738b5535b28f24d')


@router.message(Command(commands="start"))
async def start_handle(message: Message, state: FSMContext, bot: Bot):
    if message.from_user.username is not None:
        username = f"@{message.from_user.username}"
    else:
        username = message.from_user.full_name

    if not db.user_exists(message.from_user.id):
        if message.text[7:].startswith("ref"):
            ref_id = int(message.text[7:].split("_")[1])
            if ref_id != message.from_user.id:
                db.add_user(message.from_user.id, username)
                db.update_string(message.from_user.id, {'ref_id': ref_id})
                db.update_string(ref_id, {'rating': db.count_rating(ref_id)})

            else:
                await message.answer("<b>📛 Нельзя зарегистрироваться по своей реферальной ссылке!</b>")
        else:
            db.add_user(message.from_user.id, username)

    if message.text[7:] == "spamcreate":
        await message.answer(
            "🌚 <b>Выберите целевую аудиторию.</b>",
            reply_markup=choose_theme()
        )

    elif message.text[7:].startswith("lolzpay"):
        user_id = int(message.text[7:].split("_")[1])
        amount = int(message.text[7:].split("_")[2])
        comment = message.text[7:].split("_")[3]
        message_id = int(message.text[7:].split("_")[4])
        payment = lolz.market.payments.history(comment=comment)
        try:
            status = payment['payments']
            print(status)
            await bot.delete_message(message.chat.id, message_id)
            await message.answer(
                '💚 <b>Оплата Lolzteam</b>\n\n'
                f'✅ <code>{amount}</code><b>₽ переведены на твой счет.</b>'
            )
            db.update_string(user_id, {'balance': db.user_info(user_id)['balance'] + amount})
            await state.clear()
        except KeyError:
            await message.answer("📛 <b>Счет не оплачен</b>")

    else:
        await message.answer_sticker("CAACAgIAAxkBAAEKCRxk2__X8I1sEWoCtF30MhfGaPPsVgACJxwAAtqDAAFKAAG1a2gCHgiTMAQ")
        await asyncio.sleep(1)
        await message.answer(
            "📩 Многопоточная <a href='https://t.me/spamsharkbot?start=spamcreate'><b>спам-рассылка</b></a> отправит "
            "юзерам все, что тебе угодно!\n\n"
            '⚡️ Чтобы начать пользоваться ботом, нажми кнопку <b>"Меню"</b>'
        )

    await state.clear()
