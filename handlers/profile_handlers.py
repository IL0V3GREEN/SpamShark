import random
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command

from keyboards.info_buttons import main_info_buttons
from keyboards.profile_buttons import deposit_menu, payment_methods, \
    done_transaction, approving_pay, cryptopay_panel, crypto_pay_button, writing_reqs
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from mongo import Database
from utils.bank_type import check_bank
from utils.profille_functions import get_ref_percent, get_rate_status, get_reqs
from aiocryptopay import AioCryptoPay, Networks


crypto = AioCryptoPay("112126:AA1BgAlop8sbbjxEXaxFiBfaZYChxkF74pA", Networks.MAIN_NET)
db = Database()
router = Router()


class BalanceState(StatesGroup):
    amount = State()
    requisites = State()


@router.message(Command(commands="profile"))
async def balance_menu(message: Message, state: FSMContext):
    await message.answer(
        f"🥷🏻 <b>Твой профиль!</b>\n"
        f"├ 🆔<b>:</b> <code>{message.from_user.id}</code>\n"
        f"├ 📆 <b>Дата входа:</b> "
        f"<code>{db.user_info(message.from_user.id)['date']['day']}."
        f"{db.user_info(message.from_user.id)['date']['month']}."
        f"{db.user_info(message.from_user.id)['date']['year']}</code>\n"
        f"├ 💳 <b>Реквизиты:</b> <code>{get_reqs(message.from_user.id)}</code>\n"
        f"└ 🧊 <b>Баланс:</b> <code>{db.user_info(message.from_user.id)['balance']:.1f}</code>₽\n\n"
        f"📦 <b>Заказы</b>\n"
        f"├ <b>Сегодня:</b> <code>{db.count_today(message.from_user.id)}</code>\n"
        f"├ <b>За 7 дней:</b> <code>{db.count_week(message.from_user.id)}</code>\n"
        f"├ <b>За 30 дней:</b> <code>{db.count_month(message.from_user.id)}</code>\n"
        f"├ <b>Всего:</b> <code>{len(list(db.orders.find({'user_id': message.from_user.id})))}</code>\n"
        f"└ 📬 <b>Сообщений отправлено:</b> <code>{db.count_all_messages(message.from_user.id)}</code>\n\n"
        f"💥 <b>Рейтинг</b>\n"
        f"├ 🃏 <b>Статус:</b> <code>{get_rate_status(db.count_rating(message.from_user.id))}</code>\n"
        f"└ 🏆 <b>Кубков:</b> <code>{db.count_rating(message.from_user.id)}</code>\n\n"
        f"🤝 <b>Реферальная система</b>\n"
        f"├ 👥 <b>Рефералов:</b> <code>{db.count_referrals(message.from_user.id)}</code>\n"
        f"└ 💲 <b>Процент:</b> <code>{get_ref_percent(db.count_rating(message.from_user.id))}</code>%",
        reply_markup=deposit_menu(message.from_user.id)
    )
    await state.clear()


@router.callback_query(F.data.startswith("balance"))
async def balance_callback(call: CallbackQuery, state: FSMContext, bot: Bot):
    action = call.data.split("_")[1]
    if action == "deposit":
        await call.message.answer(
            "🧐 Cколько <b>₽</b> пополняем?\n\n"
            "<i>минимальное пополнение -</i> <code>100</code><i>₽</i>"
        )
        await state.set_state(BalanceState.amount)

    elif action == "withdraw":
        if db.user_info(call.from_user.id)['balance'] >= 300:
            await call.message.edit_text(
                "🗳 <b>Ваша заявка на вывод средств отправлена. "
                "Бот отправит Тебе сообщение, когда заявка будет обработана.</b>",
                reply_markup=writing_reqs()
            )
            await bot.send_message(
                call.from_user.id,
                f"Вывод\n"
                f"ID: {call.from_user.id}\n"
                f"Баланс: {db.user_info(call.from_user.id)['balance']}\n"
                f"Реквизиты: {db.user_info(call.from_user.id)['requisites']}"
            )

        else:
            await call.message.edit_text(
                "📛 <b>Минимальная сумма вывода - </b><code>300</code><b>₽</b>"
            )

    elif action == "reqs":
        await call.message.edit_text(
            "👨🏻‍🏫 <b>Ты можешь сюда ввести номеры карты, адрес крипто кошелька или номер телефона для СБП/QIWI "
            "(вместе с номером впиши банк для перевода)</b>",
            reply_markup=writing_reqs()
        )
        await state.set_state(BalanceState.requisites)


@router.message(BalanceState.requisites, F.text)
async def getting_reqs(message: Message, state: FSMContext, bot: Bot):
    db.update_string(message.from_user.id, {'requisites': message.text})
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await message.answer(
        f"🥷🏻 <b>Твой профиль!</b>\n"
        f"├ 🆔<b>:</b> <code>{message.from_user.id}</code>\n"
        f"├ 📆 <b>Дата входа:</b> "
        f"<code>{db.user_info(message.from_user.id)['date']['day']}."
        f"{db.user_info(message.from_user.id)['date']['month']}."
        f"{db.user_info(message.from_user.id)['date']['year']}</code>\n"
        f"├ 💳 <b>Реквизиты:</b> <code>{get_reqs(message.from_user.id)}</code>\n"
        f"└ 🧊 <b>Баланс:</b> <code>{db.user_info(message.from_user.id)['balance']:.1f}</code>₽\n\n"
        f"📦 <b>Заказы</b>\n"
        f"├ <b>Сегодня:</b> <code>{db.count_today(message.from_user.id)}</code>\n"
        f"├ <b>За 7 дней:</b> <code>{db.count_week(message.from_user.id)}</code>\n"
        f"├ <b>За 30 дней:</b> <code>{db.count_month(message.from_user.id)}</code>\n"
        f"├ <b>Всего:</b> <code>{len(list(db.orders.find({'user_id': message.from_user.id})))}</code>\n"
        f"└ 📬 <b>Сообщений отправлено:</b> <code>{db.count_all_messages(message.from_user.id)}</code>\n\n"
        f"💥 <b>Рейтинг</b>\n"
        f"├ 🃏 <b>Статус:</b> <code>{get_rate_status(db.count_rating(message.from_user.id))}</code>\n"
        f"└ 🏆 <b>Кубков:</b> <code>{db.count_rating(message.from_user.id)}</code>\n\n"
        f"🤝 <b>Реферальная система</b>\n"
        f"├ 👥 <b>Рефералов:</b> <code>{db.count_referrals(message.from_user.id)}</code>\n"
        f"└ 💲 <b>Процент:</b> <code>{get_ref_percent(db.count_rating(message.from_user.id))}</code>%",
        reply_markup=deposit_menu(message.from_user.id)
    )
    await state.clear()


@router.callback_query(F.data == "backfromwritting")
async def back_from_writing(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        f"🥷🏻 <b>Твой профиль!</b>\n"
        f"├ 🆔<b>:</b> <code>{call.from_user.id}</code>\n"
        f"├ 📆 <b>Дата входа:</b> "
        f"<code>{db.user_info(call.from_user.id)['date']['day']}."
        f"{db.user_info(call.from_user.id)['date']['month']}."
        f"{db.user_info(call.from_user.id)['date']['year']}</code>\n"
        f"├ 💳 <b>Реквизиты:</b> <code>{get_reqs(call.from_user.id)}</code>\n"
        f"└ 🧊 <b>Баланс:</b> <code>{db.user_info(call.from_user.id)['balance']:.1f}</code>₽\n\n"
        f"📦 <b>Заказы</b>\n"
        f"├ <b>Сегодня:</b> <code>{db.count_today(call.from_user.id)}</code>\n"
        f"├ <b>За 7 дней:</b> <code>{db.count_week(call.from_user.id)}</code>\n"
        f"├ <b>За 30 дней:</b> <code>{db.count_month(call.from_user.id)}</code>\n"
        f"├ <b>Всего:</b> <code>{len(list(db.orders.find({'user_id': call.from_user.id})))}</code>\n"
        f"└ 📬 <b>Сообщений отправлено:</b> <code>{db.count_all_messages(call.from_user.id)}</code>\n\n"
        f"💥 <b>Рейтинг</b>\n"
        f"├ 🃏 <b>Статус:</b> <code>{get_rate_status(db.count_rating(call.from_user.id))}</code>\n"
        f"└ 🏆 <b>Кубков:</b> <code>{db.count_rating(call.from_user.id)}</code>\n\n"
        f"🤝 <b>Реферальная система</b>\n"
        f"├ 👥 <b>Рефералов:</b> <code>{db.count_referrals(call.from_user.id)}</code>\n"
        f"└ 💲 <b>Процент:</b> <code>{get_ref_percent(db.count_rating(call.from_user.id))}</code>%",
        reply_markup=deposit_menu(call.from_user.id)
    )
    await state.clear()


@router.message(BalanceState.amount, F.text)
async def getting_amount(message: Message, state: FSMContext, bot: Bot):
    if message.text != '/faq':
        try:
            amount = int(message.text)
            if amount >= 1000:
                await bot.delete_message(message.chat.id, message.message_id - 1)
                await state.update_data(amount=amount)
                await message.answer(
                    f"🧾 Пополнение на {amount}₽\n\n"
                    f"<i>*Если хочешь изменить сумму пополнения, "
                    f"просто отправь другое число*</i>\n\n"
                    f"Выбери способ оплаты:",
                    reply_markup=payment_methods()
                )
            else:
                await message.answer("📛 <b>Минимальное пополнение -</b> <code>1000</code><b>₽</b>\n\n")
        except ValueError:
            await message.answer("👨🏻‍🏫 Введи целое число")
    else:
        await message.answer(
            "👨🏻‍🏫 <b>Информационная панель</b>",
            reply_markup=main_info_buttons()
        )


# choosing payment methods
@router.callback_query(F.data.startswith("method"))
async def getting_method(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")[1]
    data = await state.get_data()
    if action == "cards":
        x = random.randint(0, 4)
        card = db.functions.find_one({'my_cards': 'my_cards'})['cards'][x]
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
        caption=f"<b>Сумма перевода:</b> <code>{amount} {currency}</code>\n\n"
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
        await call.message.answer("🤥 <b>Ты не оплатил счет..</b>")

    elif invoice.status == "paid":
        await call.message.delete()
        await call.message.answer(f"<b>✅ Счет успешно пополнен на</b> <code>{amount}₽</code>")
        db.update_string(user_id, {'balance': (db.user_info(user_id)['balance'] + amount)})

        try:
            ref_id = db.user_info(user_id)['ref_id']
            award = ((amount / 100) * get_ref_percent(db.count_rating(ref_id)))
            db.update_string(
                ref_id,
                {'balance': (db.user_info(ref_id)['balance'] + award)}
            )
        except KeyError:
            pass

    elif invoice.status == "expired":
        await call.message.delete()
        await call.message.answer("⌛️ <b>Истек срок действия счета.</b>")


# sending transaction to admin
@router.callback_query(F.data.startswith("finished_transaction"))
async def sending_transaction(call: CallbackQuery, bot: Bot):
    user_id = int(call.data.split("_")[2])
    amount = int(call.data.split("_")[3])
    bank = call.data.split("_")[4]
    await call.message.edit_text(
        "<b>Перевод обрабатывается.\n\n"
        "Среднее время обработки -</b> <code>15 минут ⏳</code>"
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
            f"✅ <b>Счет успешно пополнен на</b> <code>{amount}₽</code>"
        )
        db.update_string(user_id, {'balance': (db.user_info(user_id)['balance'] + amount)})
        await call.message.edit_text(
            f"{user_id}\n"
            f"{amount}₽\n\n"
            f"Подтверждено"
        )

        try:
            ref_id = db.user_info(user_id)['ref_id']
            award = ((amount / 100) * get_ref_percent(db.count_rating(ref_id)))
            db.update_string(
                ref_id,
                {'balance': (db.user_info(ref_id)['balance'] + award)}
            )

        except KeyError:
            pass

    else:
        await bot.send_message(
            user_id,
            f"🤥 <b>Твой перевод на</b> <code>{amount}₽</code> <b>не прошел..</b>"
        )
        await call.message.edit_text(
            f"{user_id}\n"
            f"{amount}₽\n\n"
            f"Отклонено"
        )


@router.callback_query(F.data.startswith("approvewithdraw"))
async def approving_withdraw(call: CallbackQuery, bot: Bot):
    action = call.data.split("_")[1]
    user_id = int(call.data.split("_")[2])
    if action == "yes":
        await call.message.edit_text(
            f"{user_id}\n"
            f"Подтверждено"
        )
        await bot.send_message(
            user_id,
            "✔️ <b>Заявка на вывод была успешно обработана. Средства были переведены на твои реквизиты.</b>"
        )
        db.update_string(user_id, {'balance': 0})

    elif action == "no":
        await call.message.edit_text(
            f"{user_id}\n"
            f"Отклонено"
        )
        await bot.send_message(
            user_id,
            "📛 <b>Заявка на вывод была отклонена\n\n</b>"
            "🫤<b>Возможные причины:</b>\n"
            " - предоставлены неверные реквизиты"
            " - технические проблемы на стороне банка"
        )
