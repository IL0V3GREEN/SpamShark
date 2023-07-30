from aiogram.utils.keyboard import InlineKeyboardBuilder


def choose_count():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="100",
        callback_data="clientCount_100"
    )
    builder.button(
        text="500",
        callback_data="clientCount_500"
    )
    builder.button(
        text="1000",
        callback_data="clientCount_1000"
    )
    builder.button(
        text="2000",
        callback_data="clientCount_2000"
    )
    builder.button(
        text="4000",
        callback_data="clientCount_4000"
    )
    builder.button(
        text="6000",
        callback_data="clientCount_6000"
    )
    builder.button(
        text="8000",
        callback_data="clientCount_8000"
    )
    builder.button(
        text="10000",
        callback_data="clientCount_10000"
    )
    builder.button(
        text="✏️ Свое количество",
        callback_data="clientCount_self"
    )
    builder.adjust(2)
    return builder.as_markup()
