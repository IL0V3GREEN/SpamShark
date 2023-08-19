from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu(status):
    builder = InlineKeyboardBuilder()
    if status == "enabled":
        builder.button(
            text="🪚 Уйти на тех.работы",
            callback_data="admpanel_statusdisable"
        )
    else:
        builder.button(
            text="🏁 Закончить тех.работы",
            callback_data="admpanel_statusenable"
        )
    builder.button(
        text="📊 Статистика",
        callback_data="admpanel_stats"
    )
    builder.adjust(1)
    return builder.as_markup()
