from aiogram.utils.keyboard import InlineKeyboardBuilder
from mongo import Database


db = Database()


def deposit_menu(user_id):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🏧 Пополнить баланс",
        callback_data="balance_deposit"
    )
    try:
        reqs = db.user_info(user_id)['requisites']
        builder.button(
            text="💰 Вывести средства",
            callback_data="balance_withdraw"
        )
    except KeyError:
        pass
    builder.button(
        text="🔄 Обновить реквизиты",
        callback_data="balance_reqs"
    )
    builder.adjust(1)
    return builder.as_markup()


def writing_reqs():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Назад",
        callback_data="backfromwritting"
    )
    builder.adjust(1)
    return builder.as_markup()


def crypto_pay_button(url, amount, currency, invoice_id, user_id, rubles):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Оплатить {amount} {currency}",
        url=url
    )
    builder.button(
        text="✅ Я оплатил",
        callback_data=f"ihavepaid_{invoice_id}_{user_id}_{rubles}"
    )
    builder.adjust(1)
    return builder.as_markup()


def payment_methods():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🇷🇺 Cards RU",
        callback_data="method_cards"
    )
    builder.button(
        text="Crypto",
        callback_data="method_crypto"
    )
    builder.adjust(1)
    return builder.as_markup()


def done_transaction(user_id, amount, bank):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✔️ Я перевел",
        callback_data="finished_transaction_" + f"{user_id}_" + f"{amount}_" + f"{bank}"
    )
    return builder.as_markup()


def approving_pay(user_id, amount):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Подтвердить",
        callback_data="processpay_accept_" + f"{user_id}_" + f"{amount}"
    )
    builder.button(
        text="Отклонить",
        callback_data="processpay_deny_" + f"{user_id}_" + f"{amount}"
    )
    builder.adjust(1)
    return builder.as_markup()


def approving_withdraw(user_id):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Подтвердить",
        callback_data=f"approvewithdraw_yes_{user_id}"
    )
    builder.button(
        text="Отклонить",
        callback_data=f"approvewithdraw_no_{user_id}"
    )
    builder.adjust(1)
    return builder.as_markup()


def cryptopay_panel(currency_list):
    builder = InlineKeyboardBuilder()
    for i in currency_list:
        builder.button(
            text=f"{i.source}",
            callback_data=f"paycryptobot_{i.source}_" + f"{i.rate}"
        )
    builder.adjust(3)
    return builder.as_markup()
