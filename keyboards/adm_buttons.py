from aiogram.utils.keyboard import InlineKeyboardBuilder


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
    builder.adjust(1)
    return builder.as_markup()


def adm_back_from_stats():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Назад",
        callback_data="admback"
    )
    return builder.as_markup()
