from aiogram.utils.keyboard import InlineKeyboardBuilder


def support_link():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="☎️ Поддержка",
        url="https://t.me/maximus_cls"
    )
    return builder.as_markup()
