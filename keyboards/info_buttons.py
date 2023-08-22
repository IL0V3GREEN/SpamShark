from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_info_buttons():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🏆 Рейтинговая система",
        callback_data="info_rating"
    )
    builder.button(
        text="🤼‍♂️ ТОП - пользователей",
        callback_data="info_top"
    )
    builder.button(
        text="💬 Где оставить отзыв",
        callback_data="info_review"
    )
    builder.button(
        text="☎️ Поддержка",
        url="https://t.me/maximus_cls"
    )
    builder.adjust(1)
    return builder.as_markup()


def back_from_stats(username):
    builder = InlineKeyboardBuilder()
    if username != 'Скрыт':
        builder.button(
            text="🙈 Скрыть себя",
            callback_data="topmake_invisible"
        )
    else:
        builder.button(
            text="👀 Отображать себя",
            callback_data="topmake_visible"
        )
    builder.button(
        text="🔙 Назад",
        callback_data="rating_back"
    )
    builder.adjust(1)
    return builder.as_markup()


def rating_buttons():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="❔ Как повышать рейтинг",
        callback_data="rating_increase"
    )
    builder.button(
        text="🔙 Назад",
        callback_data="rating_back"
    )
    builder.adjust(1)
    return builder.as_markup()


def review_buttons():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="📌 Наша тема на LOLZ",
        url='https://zelenka.guru/threads/5714798/'
    )
    builder.button(
        text="🔙 Назад",
        callback_data="rating_back"
    )
    builder.adjust(1)
    return builder.as_markup()


def how_to_increase_button():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🔙 Назад",
        callback_data="increaseback"
    )
    builder.adjust(1)
    return builder.as_markup()
