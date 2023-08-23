from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from mongo import Database
from utils.profille_functions import get_price

db = Database()


class EditFactory(CallbackData, prefix="editfab"):
    action: str
    url: bool
    text: bool
    media: bool


def edit_sets(
        user_id: int, text: bool, media: bool, url: bool, theme: str, count: int, url_buttons: list | None = None
):
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
        text=f"Кол-во сообщений: {count} ({get_price(db.user_info(user_id)['rating']) * count}₽)",
        callback_data="spambuild_count"
    )
    builder.button(
        text="Подтвердить",
        callback_data=EditFactory(action="finish", text=text, url=url, media=media)
    )
    builder.button(
        text="🔙 Выйти",
        callback_data="exitFromBuilder"
    )
    builder.adjust(1)
    return builder.as_markup()


def client_finish_buttons(url: list):
    builder = InlineKeyboardBuilder()
    for i in url:
        builder.button(
            text=f"{(i.split('-')[0])[:-1]}",
            url=f"{(i.split('-')[1])[1:]}"
        )
    builder.adjust(1)
    return builder.as_markup()


def admin_spam_end(url: list | None = None):
    builder = InlineKeyboardBuilder()
    for i in url:
        builder.button(
            text=f"{(i.split('-')[0])[:-1]}",
            url=f"{(i.split('-')[1])[1:]}"
        )
    builder.button(
        text="Спам-рассылка завершена",
        callback_data=f"endSpam"
    )
    builder.adjust(1)
    return builder.as_markup()


def choose_theme():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🏦 Финансы & Криптовалюта",
        callback_data="spamtype_finance&crypto"
    )
    builder.button(
        text="🤠 Юмор и Развлечения",
        callback_data="spamtype_humor&games"
    )
    builder.button(
        text="🎭 Политика",
        callback_data="spamtype_politics"
    )
    builder.button(
        text="🧬 Технологии",
        callback_data="spamtype_tech"
    )
    builder.button(
        text="💊 Медицина",
        callback_data="spamtype_medicine"
    )
    builder.button(
        text="🔞 Dating & Porn",
        callback_data="spamtype_adult"
    )
    builder.button(
        text="🌐 Даркнет",
        callback_data="spamtype_darknet"
    )
    builder.button(
        text="➡️ Skip",
        callback_data="spamtype_skipped"
    )
    builder.adjust(1)
    return builder.as_markup()


def choose_count():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="250",
        callback_data="clientCount_250"
    )
    builder.button(
        text="1000",
        callback_data="clientCount_1000"
    )
    builder.button(
        text="5000",
        callback_data="clientCount_5000"
    )
    builder.button(
        text="10000",
        callback_data="clientCount_10000"
    )
    builder.button(
        text="15000",
        callback_data="clientCount_15000"
    )
    builder.button(
        text="25000",
        callback_data="clientCount_25000"
    )
    builder.button(
        text="35000",
        callback_data="clientCount_35000"
    )
    builder.button(
        text="50000",
        callback_data="clientCount_50000"
    )
    builder.button(
        text="✏️ Свое количество",
        callback_data="clientCount_self"
    )
    builder.adjust(2)
    return builder.as_markup()

