import asyncio
import random
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards.balance_buttons import deposit_menu, payment_methods, done_transaction, approving_pay
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from mongo import Database
from utils.bank_type import check_bank
from aiocryptopay import AioCryptoPay, Networks


crypto = AioCryptoPay("112126:AA1BgAlop8sbbjxEXaxFiBfaZYChxkF74pA", Networks.MAIN_NET)
db = Database()
router = Router()


class BalanceState(StatesGroup):
    amount = State()


@router.message(Command(commands="balance"))
async def balance_menu(message: Message):
    await message.answer(
        f"👤 ID: <tg-spoiler>{message.from_user.id}</tg-spoiler>\n\n"
        f"Баланс: <b>{db.user_info(message.from_user.id)['balance']:.2f}₽</b>\n\n"
        f"🏦 <b>Cards, Crypto, BinancePay</b>",
        reply_markup=deposit_menu()
    )


@router.callback_query(F.data.startswith("balance"))
async def balance_callback(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")[1]
    if action == "deposit":
        builder = ReplyKeyboardBuilder()
        builder.button(text="Отменить оплату")
        await call.message.answer(
            "🧐 На сколько <b>₽</b> пополняем?\n\n"
            "<i>минимальное пополнение - 100₽</i>",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
        await state.set_state(BalanceState.amount)

    elif action == "ref":
        pass


@router.message(BalanceState.amount, F.text)
async def getting_amount(message: Message, state: FSMContext):
    if message.text != "Отменить оплату":
        try:
            amount = int(message.text)
            if amount >= 100:
                await state.update_data(amount=amount)
                await message.answer(
                    f"🧾 <b>Пополнение на {amount}₽</b>\n\n"
                    f"<i>*Если хотите изменить сумму пополнения,\n"
                    f"просто отправьте другое число*</i>\n\n"
                    f"Выберите способ оплаты:",
                    reply_markup=payment_methods()
                )

            else:
                await message.answer("📛 Минимальное пополнение - <b>100₽</b>")

        except ValueError:
            await message.answer("👨🏻‍🏫 Введите целое число")

    else:
        await message.answer("Пополнение отменено", reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(1)
        await message.answer(
            f"👤 ID: <tg-spoiler>{message.from_user.id}</tg-spoiler>\n\n"
            f"Баланс: <b>{db.user_info(message.from_user.id)['balance']}₽</b>\n\n"
            f"🏦 <b>Cards, Crypto, BinancePay</b>",
            reply_markup=deposit_menu()
        )


# choosing payment methods
@router.callback_query(F.data.startswith("method"))
async def getting_method(call: CallbackQuery, state: FSMContext, bot: Bot):
    action = call.data.split("_")[1]
    data = await state.get_data()
    if action == "cards":
        x = random.randint(0, 4)
        card = db.collection.find_one({'my_cards': 'my_cards'})['cards'][x]
        bank = check_bank(card)
        await call.message.edit_text(
            f"<i><b>{bank}</b></i>\n\n"
            f"<b>Пополнение на {data['amount']}₽</b>\n"
            f"Номер карты: <code>{card}</code>\n\n"
            f"<i>нажми на кнопку после успешного перевода средств</i>",
            reply_markup=done_transaction(call.from_user.id, data['amount'], bank)
        )

    elif action == "binance":
        pass

    elif action == "crypto":
        print(await crypto.get_currencies())
        print(await crypto.get_exchange_rates())


# sending transaction to admin
@router.callback_query(F.data.startswith("finished_transaction"))
async def sending_transaction(call: CallbackQuery, bot: Bot):
    user_id = int(call.data.split("_")[2])
    amount = int(call.data.split("_")[3])
    bank = call.data.split("_")[4]
    await call.message.edit_text(
        "<b>Твой перевод обрабатывается</b>\n\n"
        "Среднее время обработки - 15 минут ⏳"
    )
    await bot.send_message(
        6364771832,
        f"Bank: {bank}\n"
        f"Amount: {amount}\n"
        f"user_id: {user_id}",
        reply_markup=approving_pay(user_id, amount)
    )


# Admin approving payment
@router.callback_query(F.data.startswith("processpay"))
async def approving_transaction(call: CallbackQuery, bot: Bot):
    action = call.data.split("_")[1]
    user_id = int(call.data.split("_")[2])
    amount = int(call.data.split("_")[3])
    if action == "accept":
        await bot.send_message(
            user_id,
            f"✅ Твой счет успешно пополнен на <b>{amount}₽</b>",
            reply_markup=ReplyKeyboardRemove()
        )
        db.update_string(user_id, {'balance': (db.user_info(user_id)['balance'] + amount)})
        await call.message.edit_text(
            f"{user_id}\n"
            f"{amount}₽\n\n"
            f"Подтверждено"
        )
    else:
        await bot.send_message(
            user_id,
            f"🤥 Твой перевод на <b>{amount}₽</b> не прошел..",
            reply_markup=ReplyKeyboardRemove()
        )
        await call.message.edit_text(
            f"{user_id}\n"
            f"{amount}₽\n\n"
            f"Отклонено"
        )
