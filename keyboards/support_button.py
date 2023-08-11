from aiogram.utils.keyboard import InlineKeyboardBuilder


def support_link():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="☎️ Поддержка",
        url="https://t.me/rrassvetov"
    )
    return builder.as_markup()
