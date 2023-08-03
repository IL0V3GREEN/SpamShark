from aiogram.utils.keyboard import InlineKeyboardBuilder


def deposit_menu():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Пополнить",
        callback_data="balance_deposit"
    )
    builder.button(
        text="Реферальная система",
        callback_data="balance_ref"
    )
    builder.adjust(1)
    return builder.as_markup()


def crypto_pay_button(url, amount, currency):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Оплатить {amount} {currency}",
        url=url
    )
    builder.button(
        text="🔙 Назад",
        callback_data="back_to_crypto_list"
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
        text="BinancePay",
        callback_data="method_binance"
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


def cryptopay_panel(currency_list):
    builder = InlineKeyboardBuilder()
    for i in currency_list:
        builder.button(
            text=f"{i.source}",
            callback_data=f"paycryptobot_{i.source}_" + f"{i.rate}"
        )
    builder.adjust(3)
    return builder.as_markup()
