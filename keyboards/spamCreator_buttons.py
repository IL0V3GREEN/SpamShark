from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class EditFactory(CallbackData, prefix="editfab"):
    action: str
    url: bool
    text: bool
    media: bool


def edit_sets(text: bool, media: bool, url: bool, theme: str, count: int, url_buttons: list or None = None):
    builder = InlineKeyboardBuilder()
    if url is True:
        if url_buttons is not None:
            for i in url_buttons:
                builder.button(
                    text=f"{(i.split('-')[0])[:-1]}",
                    url=f"{(i.split('-')[1])[1:]}"
                )
    if not text:
        builder.button(
            text="Добавить текст",
            callback_data=EditFactory(action="text_add", text=text, url=url, media=media)
        )
    if text:
        builder.button(
            text="Удалить текст",
            callback_data=EditFactory(action="text_delete", text=text, url=url, media=media)
        )
    if not media:
        builder.button(
            text="Добавить медиафайл",
            callback_data=EditFactory(action="media_add", text=text, url=url, media=media)
        )
    if media:
        builder.button(
            text="Удалить медиафайл",
            callback_data=EditFactory(action="media_delete", text=text, url=url, media=media)
        )
    if not url:
        builder.button(
            text="Добавить URL-кнопки",
            callback_data=EditFactory(action="url_add", text=text, url=url, media=media)
        )
    if url:
        builder.button(
            text="Удалить URL-кнопки",
            callback_data=EditFactory(action="url_delete", text=text, url=url, media=media)
        )

    builder.button(
        text=f"Целевая аудитория: {theme}",
        callback_data="spambuild_theme"
    )
    builder.button(
        text=f"Количество сообщений: {count}",
        callback_data="spambuild_count"
    )
    builder.button(
        text="Подтвердить",
        callback_data=EditFactory(action="finish", text=text, url=url, media=media)
    )
    builder.adjust(1)
    return builder.as_markup()


def exit_from_builder():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🔚 Выйти из билдера")
    return builder.as_markup(resize_keyboard=True)


def client_finish_buttons(url: list):
    builder = InlineKeyboardBuilder()
    for i in url:
        builder.button(
            text=f"{(i.split('-')[0])[:-1]}",
            url=f"{(i.split('-')[1])[1:]}"
        )


def admin_spam_start(url: list | None = None):
    builder = InlineKeyboardBuilder()
    if url is not None:
        for i in url:
            builder.button(
                text=f"{(i.split('-')[0])[:-1]}",
                url=f"{(i.split('-')[1])[1:]}"
            )
    builder.button(
        text="😤 Приступить спамить",
        callback_data="start_spam"
    )
    builder.adjust(1)
    return builder.as_markup()

