from aiogram.utils.keyboard import InlineKeyboardBuilder
from mongo import Database


db = Database()


def main_menu(status):
    builder = InlineKeyboardBuilder()
    if status == "enabled":
        builder.button(
            text="🪚 Уйти на тех.работы",
            callback_data="admpanel_statuschange"
        )
    else:
        builder.button(
            text="🏁 Закончить тех.работы",
            callback_data="admpanel_statuschange"
        )
    builder.button(
        text="📊 Статистика",
        callback_data="admpanel_stats"
    )
    builder.button(
        text="✉️ Создать рассылку",
        callback_data="admpanel_message"
    )
    # builder.button(
    #     text="📱 Менеджер аккаунтов",
    #     callback_data="admpanel_accounts"
    # )
    builder.button(
        text="🌐 Менеджер прокси",
        callback_data="admpanel_proxy"
    )
    builder.adjust(1)
    return builder.as_markup()


def proxy_buttons():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🆕 Добавить прокси",
        callback_data="proxy_add"
    )
    builder.button(
        text="🔙 Назад",
        callback_data="admback"
    )
    builder.adjust(1)
    return builder.as_markup()


def tg_sets():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🆕 Добавить аккаунт",
        callback_data="tgsets_add"
    )
    builder.button(
        text="🧩 Валидность аккаунтов",
        callback_data="tgsets_check"
    )
    builder.button(
        text="🔙 Назад",
        callback_data="admback"
    )
    builder.adjust(1)
    return builder.as_markup()


def back_to_account_manager():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Отменить",
        callback_data="toAccManager"
    )
    return builder.as_markup()


def adm_back_from_stats():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Назад",
        callback_data="admback"
    )
    return builder.as_markup()
