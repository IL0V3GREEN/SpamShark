from aiogram.utils.keyboard import InlineKeyboardBuilder


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
        callback_data="spamtype_skip"
    )
    builder.adjust(1)
    return builder.as_markup()
