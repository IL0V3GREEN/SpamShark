
import random
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from keyboards.balance_buttons import deposit_menu, payment_methods, \
    done_transaction, approving_pay, cryptopay_panel, crypto_pay_button
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


@router.message(Command(commands="profile"))
async def balance_menu(message: Message, state: FSMContext):
    await message.answer(
        f"🥷🏻<b>Твой профиль!</b>\n"
        f"├ 🆔<b>ID:</b> <code>{message.from_user.id}</code>\n"
        f"└ 💎<b>Баланс:</b> {db.user_info(message.from_user.id)['balance']:.2f}₽\n\n"
        f"🤝<b>Реферальная система:</b>\n"
        f"├ 👥<b>Рефералы:</b> {db.count_referrals(message.from_user.id)}\n"
        f"├ 🧊<b>Профит с рефералов:</b> 10%\n"
        f"└ 📎<b>Ссылка:</b> <code>https://t.me/spamsharkbot?start=ref_{message.from_user.id}</code>",
        reply_markup=deposit_menu()
    )
    await state.clear()


@router.callback_query(F.data.startswith("balance"))
async def balance_callback(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")[1]
    if action == "deposit":
        await call.message.answer(
            "🧐 Cколько <b>₽</b> пополняем?\n\n"
            "<i>минимальное пополнение - 100₽</i>"
        )
        await state.set_state(BalanceState.amount)


@router.message(BalanceState.amount, F.text)
async def getting_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount >= 100:
            await state.update_data(amount=amount)
            await message.answer(
                f"🧾 Пополнение на {amount}₽\n\n"
                f"<i>*Если хочешь изменить сумму пополнения, "
                f"просто отправь другое число*</i>\n\n"
                f"Выбери способ оплаты:",
                reply_markup=payment_methods()
            )
        else:
            await message.answer("📛 Минимальное пополнение - 100₽")
    except ValueError:
        await message.answer("👨🏻‍🏫 Введи целое число")


# choosing payment methods
@router.callback_query(F.data.startswith("method"))
async def getting_method(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")[1]
    data = await state.get_data()
    if action == "cards":
        x = random.randint(0, 4)
        card = db.collection.find_one({'my_cards': 'my_cards'})['cards'][x]
        bank = check_bank(card)
        await call.message.edit_text(
            f"🏦 <i><b>{bank}</b></i>\n\n"
            f"Сумма перевода: {data['amount']}₽\n"
            f"Номер карты: <code>{card}</code>\n\n"
            f"<i>нажми на кнопку после успешного перевода</i>",
            reply_markup=done_transaction(call.from_user.id, data['amount'], bank)
        )

    elif action == "crypto":
        x = await crypto.get_exchange_rates()
        currency_list = []
        for i in x:
            if i.target == "RUB":
                currency_list.append(i)
        await call.message.edit_text(
            "Выбери криптовалюуту:",
            reply_markup=cryptopay_panel(currency_list)
        )


@router.callback_query(F.data.startswith("paycryptobot"))
async def crypto_payment(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    currency = call.data.split("_")[1]
    rate = float(call.data.split("_")[2])
    amount = ""
    if currency in ["USDT", "TON", "BUSD", "TRX", "USDC", "BNB"]:
        amount = f"{(data['amount'] / rate):.3f}"
    if currency in ["BTC", "ETH"]:
        amount = f"{(data['amount'] / rate):.7f}"

    invoice = await crypto.create_invoice(
        currency,
        float(amount),
        paid_btn_name="openBot",
        paid_btn_url="https://t.me/spamsharkbot",
        expires_in=1800
    )
    photo = FSInputFile("data/photo.jpeg")
    await call.message.delete()
    await call.message.answer_photo(
        photo=photo,
        caption=f"Сумма перевода: {amount} {currency}\n\n"
                f"<i>счет действителен в течении 30 минут ⏳</i>",
        reply_markup=crypto_pay_button(
            invoice.pay_url,
            amount,
            currency,
            invoice.invoice_id,
            call.from_user.id,
            data['amount']
        )
    )


@router.callback_query(F.data.startswith("ihavepaid"))
async def approving_cryptopay(call: CallbackQuery):
    invoice_id = int(call.data.split("_")[1])
    user_id = int(call.data.split("_")[2])
    amount = int(call.data.split("_")[3])
    invoice = await crypto.get_invoices(invoice_ids=invoice_id)
    if invoice.status == "active":
        await call.message.answer("🤥 Ты не оплатил счет..")

    elif invoice.status == "paid":
        await call.message.delete()
        await call.message.answer(f"✅ Счет успешно пополнен на {amount}₽.")
        db.update_string(
            user_id,
            {'balance': (db.user_info(user_id)['balance'] + amount)}
        )

        try:
            ref_id = db.user_info(user_id)['ref_id']
            db.update_string(
                ref_id,
                {'balance': (db.user_info(ref_id)['balance'] + (amount * 0.1))}
            )
        except KeyError:
            pass

    elif invoice.status == "expired":
        await call.message.delete()
        await call.message.answer("⌛️ Истек срок действия счета.")


# sending transaction to admin
@router.callback_query(F.data.startswith("finished_transaction"))
async def sending_transaction(call: CallbackQuery, bot: Bot):
    user_id = int(call.data.split("_")[2])
    amount = int(call.data.split("_")[3])
    bank = call.data.split("_")[4]
    await call.message.edit_text(
        "Перевод обрабатывается.\n\n"
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
            f"✅ Счет успешно пополнен на {amount}₽"
        )
        db.update_string(user_id, {'balance': (db.user_info(user_id)['balance'] + amount)})
        await call.message.edit_text(
            f"{user_id}\n"
            f"{amount}₽\n\n"
            f"Подтверждено"
        )

        try:
            ref_id = db.user_info(user_id)['ref_id']
            db.update_string(
                ref_id,
                {'balance': (db.user_info(ref_id)['balance'] + (amount * 0.1))}
            )
        except KeyError:
            pass

    else:
        await bot.send_message(
            user_id,
            f"🤥 Твой перевод на {amount}₽ не прошел.."
        )
        await call.message.edit_text(
            f"{user_id}\n"
            f"{amount}₽\n\n"
            f"Отклонено"
        )
