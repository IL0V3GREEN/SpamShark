from aiogram.utils.keyboard import InlineKeyboardBuilder


def where_spamming():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="📬 Участников открытой группы",
        callback_data="parsetype_chat"
    )
    builder.button(
        text="💎 Комментаторов открытого канала",
        callback_data="parsetype_channel"
    )
    builder.adjust(1)
    return builder.as_markup()
