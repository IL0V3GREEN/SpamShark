from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, InputMedia, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from keyboards.profile_buttons import deposit_menu
from keyboards.spamCreator_buttons import edit_sets, EditFactory, admin_spam_start, client_finish_buttons, \
    choose_theme, choose_count, admin_spam_end
from utils.check_state import check_text, check_media, check_inline
from mongo import Database
import random
from utils.profille_functions import get_rate_status, get_ref_percent, get_reqs, get_price

db = Database()
router = Router()


class UserState(StatesGroup):
    spam_theme = State()
    message_count = State()
    client_text = State()
    text = State()
    media = State()
    inline = State()


@router.message(Command(commands="spam"))
async def start_spam_creating(message: Message, state: FSMContext):
    await message.answer(
        "🌚 Выбери целевую аудиторию.",
        reply_markup=choose_theme()
    )
    await state.clear()


@router.callback_query(F.data.startswith("spamtype"))
async def getting_type(call: CallbackQuery, state: FSMContext):
    theme = call.data.split("_")[1]
    await state.update_data(spam_theme=theme)
    data = await state.get_data()
    text = await check_text(data)
    media = await check_media(data)
    buttons = await check_inline(data)

    # text & media & buttons
    if text and media and buttons:
        await call.message.delete()
        await call.message.answer_photo(
            photo=data['media'],
            caption=data['text'],
            reply_markup=edit_sets(
                True, True, True, data['spam_theme'], data['message_count'], url_buttons=data['inline']
            )
        )
        await state.set_state(UserState.client_text)
    # text & media
    elif text and media and not buttons:
        await call.message.delete()
        await call.message.answer_photo(
            photo=data['media'],
            caption=data['text'],
            reply_markup=edit_sets(
                True, True, False, data['spam_theme'], data['message_count']
            )
        )
        await state.set_state(UserState.client_text)
    # text & buttons
    elif text and buttons and not media:
        await call.message.edit_text(
            data['text'],
            reply_markup=edit_sets(
                True, False, True, data['spam_theme'], data['message_count'], url_buttons=data['inline']
            )
        )
        await state.set_state(UserState.client_text)
    # media & buttons
    elif media and buttons and not text:
        await call.message.delete()
        await call.message.answer_photo(
            photo=data['media'],
            reply_markup=edit_sets(
                False, True, True, data['spam_theme'], data['message_count'], url_buttons=data['inline']
            )
        )
        await state.set_state(UserState.client_text)
    # just media
    elif media and not text and not buttons:
        await call.message.delete()
        await call.message.answer_photo(
            photo=data['media'],
            reply_markup=edit_sets(
                False, True, False, data['spam_theme'], data['message_count']
            )
        )
        await state.set_state(UserState.client_text)
    # just text
    elif text and not buttons and not media:
        await call.message.edit_text(
            data['text'],
            reply_markup=edit_sets(
                True, False, False, data['spam_theme'], data['message_count']
            )
        )
        await state.set_state(UserState.client_text)
    else:
        await call.message.edit_text(
            "🔢 Выбери количество сообщений.\n\n"
            f"<i>1 сообщение = <code>{get_price(db.count_rating(call.from_user.id))}</code>₽</i>",
            reply_markup=choose_count()
        )
        await state.set_state(UserState.message_count)


@router.callback_query(UserState.message_count, F.data.startswith("clientCount"))
async def getting_count(call: CallbackQuery, state: FSMContext):
    if call.data != "clientCount_self":
        count = int(call.data.split("_")[1])
        await state.update_data(message_count=count)
        data = await state.get_data()

        text = await check_text(data)
        media = await check_media(data)
        buttons = await check_inline(data)

        # text & media & buttons
        if text and media and buttons:
            await call.message.delete()
            await call.message.answer_photo(
                photo=data['media'],
                caption=data['text'],
                reply_markup=edit_sets(
                    True, True, True, data['spam_theme'], data['message_count'], url_buttons=data['inline']
                )
            )
            await state.set_state(UserState.client_text)
        # text & media
        elif text and media and not buttons:
            await call.message.delete()
            await call.message.answer_photo(
                photo=data['media'],
                caption=data['text'],
                reply_markup=edit_sets(
                    True, True, False, data['spam_theme'], data['message_count']
                )
            )
            await state.set_state(UserState.client_text)
        # text & buttons
        elif text and buttons and not media:
            await call.message.edit_text(
                data['text'],
                reply_markup=edit_sets(
                    True, False, True, data['spam_theme'], data['message_count'], url_buttons=data['inline']
                )
            )
            await state.set_state(UserState.client_text)
        # media & buttons
        elif media and buttons and not text:
            await call.message.delete()
            await call.message.answer_photo(
                photo=data['media'],
                reply_markup=edit_sets(
                    False, True, True, data['spam_theme'], data['message_count'], url_buttons=data['inline']
                )
            )
            await state.set_state(UserState.client_text)
        # just media
        elif media and not text and not buttons:
            await call.message.delete()
            await call.message.answer_photo(
                photo=data['media'],
                reply_markup=edit_sets(
                    False, True, False, data['spam_theme'], data['message_count']
                )
            )
            await state.set_state(UserState.client_text)
        # just text
        elif text and not buttons and not media:
            await call.message.edit_text(
                data['text'],
                reply_markup=edit_sets(
                    True, False, False, data['spam_theme'], data['message_count']
                )
            )
            await state.set_state(UserState.client_text)

        else:
            await call.message.edit_text(
                "Отправь боту то, что будет рассылаться пользователям.\n"
                "Это может быть все, что угодно - текст, фото."
            )
            await state.set_state(UserState.client_text)

    else:
        await call.message.edit_text(
            "📝 Введи свое количество: \n\n"
            f"<i>1 сообщение = <code>{get_price(db.count_rating(call.from_user.id))}</code>₽</i>"
        )


@router.message(UserState.message_count, F.text)
async def getting_self_count(message: Message, state: FSMContext, bot: Bot):
    if message.text != "/profile":
        count = message.text
        try:
            count = int(count)
            if count <= 10000:
                await bot.delete_message(message.chat.id, message.message_id - 1)
                await state.update_data(message_count=count)
                data = await state.get_data()

                text = await check_text(data)
                media = await check_media(data)
                buttons = await check_inline(data)

                # text & media & buttons
                if text and media and buttons:
                    await message.delete()
                    await message.answer_photo(
                        photo=data['media'],
                        caption=data['text'],
                        reply_markup=edit_sets(
                            True, True, True, data['spam_theme'], data['message_count'], url_buttons=data['inline']
                        )
                    )
                    await state.set_state(UserState.client_text)
                # text & media
                elif text and media and not buttons:
                    await message.delete()
                    await message.answer_photo(
                        photo=data['media'],
                        caption=data['text'],
                        reply_markup=edit_sets(
                            True, True, False, data['spam_theme'], data['message_count']
                        )
                    )
                    await state.set_state(UserState.client_text)
                # text & buttons
                elif text and buttons and not media:
                    await message.edit_text(
                        data['text'],
                        reply_markup=edit_sets(
                            True, False, True, data['spam_theme'], data['message_count'], url_buttons=data['inline']
                        )
                    )
                    await state.set_state(UserState.client_text)
                # media & buttons
                elif media and buttons and not text:
                    await message.delete()
                    await message.answer_photo(
                        photo=data['media'],
                        reply_markup=edit_sets(
                            False, True, True, data['spam_theme'], data['message_count'], url_buttons=data['inline']
                        )
                    )
                    await state.set_state(UserState.client_text)
                # just media
                elif media and not text and not buttons:
                    await message.delete()
                    await message.answer_photo(
                        photo=data['media'],
                        reply_markup=edit_sets(
                            False, True, False, data['spam_theme'], data['message_count']
                        )
                    )
                    await state.set_state(UserState.client_text)
                # just text
                elif text and not buttons and not media:
                    await message.edit_text(
                        data['text'],
                        reply_markup=edit_sets(
                            True, False, False, data['spam_theme'], data['message_count']
                        )
                    )
                    await state.set_state(UserState.client_text)

                else:
                    await message.answer(
                        "Отправь боту то, что будет рассылаться пользователям.\n"
                        "Это может быть все, что угодно - текст, фото"
                    )
                    await state.set_state(UserState.client_text)
            else:
                await message.answer("📛 Максимальное значение - 10.000")

        except ValueError:
            await message.answer(
                "📛 Введи корректное значение."
            )

    else:
        await message.answer("🔚 Ты вышел из спам-билдера.")
        await message.answer(
            f"🥷🏻 <b>Твой профиль!</b>\n"
            f"├ 🆔<b>:</b> <code>{message.from_user.id}</code>\n"
            f"├ 💳 <b>Реквизиты:</b> <code>{get_reqs(message.from_user.id)}</code>\n"
            f"└ 🧊 <b>Баланс:</b> <code>{db.user_info(message.from_user.id)['balance']:.1f}</code>₽\n\n"
            f"📦 <b>Заказы</b>\n"
            f"├ <b>Сегодня:</b> <code>{db.count_today(message.from_user.id)}</code>\n"
            f"├ <b>За 7 дней:</b> <code>{db.count_week(message.from_user.id)}</code>\n"
            f"├ <b>За 30 дней:</b> <code>{db.count_month(message.from_user.id)}</code>\n"
            f"├ <b>Всего:</b> <code>{len(list(db.orders.find({'user_id': message.from_user.id})))}</code>\n"
            f"└ 📬 <b>Сообщений отправлено:</b> <code>{db.count_all_messages(message.from_user.id)}</code>\n\n"
            f"💥 <b>Рейтинг</b>\n"
            f"├ 🃏 <b>Статус:</b> <code>{get_rate_status(db.count_rating(message.from_user.id))}</code>\n"
            f"└ 🏆 <b>Кубков:</b> <code>{db.count_rating(message.from_user.id)}</code>\n\n"
            f"🤝 <b>Реферальная система</b>\n"
            f"├ 👥 <b>Рефералов:</b> <code>{db.count_referrals(message.from_user.id)}</code>\n"
            f"└ 💲 <b>Процент:</b> <code>{get_ref_percent(db.count_rating(message.from_user.id))}</code>%",
            reply_markup=deposit_menu(message.from_user.id)
        )
        await state.clear()


@router.message(UserState.client_text, F.photo | F.video)
async def getting_text(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    text = await check_text(data)
    buttons = await check_inline(data)

    await bot.delete_message(message.chat.id, message.message_id - 1)
    if text and buttons:
        try:
            await message.answer_photo(
                message.photo[0].file_id,
                caption=data['text'],
                reply_markup=edit_sets(
                    True,
                    True,
                    True,
                    data['spam_theme'],
                    data['message_count'],
                    data['inline']
                )
            )
            await state.update_data(media=message.photo[0].file_id)
        except AttributeError:
            await message.answer(
                "😕 Видео содержащие спам-рассылки пока недоступны"
            )
    elif text and not buttons:
        try:
            await message.answer_photo(
                message.photo[0].file_id,
                caption=data['text'],
                reply_markup=edit_sets(
                    True,
                    True,
                    False,
                    data['spam_theme'],
                    data['message_count']
                )
            )
            await state.update_data(media=message.photo[0].file_id)
        except AttributeError:
            await message.answer(
                "😕 Видео содержащие спам-рассылки пока недоступны"
            )

    elif not text and buttons:
        try:
            await message.answer_photo(
                message.photo[0].file_id,
                reply_markup=edit_sets(
                    False,
                    True,
                    True,
                    data['spam_theme'],
                    data['message_count'],
                    data['inline']
                )
            )
            await state.update_data(media=message.photo[0].file_id)
        except AttributeError:
            await message.answer(
                "😕 Видео содержащие спам-рассылки пока недоступны"
            )
    else:
        try:
            await message.answer_photo(
                message.photo[0].file_id,
                reply_markup=edit_sets(
                    False,
                    True,
                    False,
                    data['spam_theme'],
                    data['message_count']
                )
            )
            await state.update_data(media=message.photo[0].file_id)
        except AttributeError:
            await message.answer(
                "😕 Видео содержащие спам-рассылки пока недоступны"
            )
    await state.set_state(UserState.client_text)


@router.message(UserState.client_text, F.text)
async def getting_text(message: Message, state: FSMContext, bot: Bot):
    if message.text != '/profile':
        data = await state.get_data()

        media = await check_media(data)
        buttons = await check_inline(data)

        await bot.delete_message(message.chat.id, message.message_id - 1)
        if media and buttons:
            await message.answer_photo(
                photo=data['media'],
                caption=message.text,
                reply_markup=edit_sets(
                    True, True, True, data['spam_theme'], data['message_count'], data['inline']
                )
            )
            await state.update_data(text=message.text)

        elif media and not buttons:
            await message.answer_photo(
                photo=data['media'],
                caption=message.text,
                reply_markup=edit_sets(
                    True, True, False, data['spam_theme'], data['message_count']
                )
            )
            await state.update_data(text=message.text)
        elif not media and buttons:
            await message.answer(
                message.text,
                reply_markup=edit_sets(
                    True, False, True, data['spam_theme'], data['message_count'], data['inline']
                )
            )
            await state.update_data(text=message.text)

        elif not media and not buttons:
            await message.answer(
                message.text,
                reply_markup=edit_sets(
                    True, False, False, data['spam_theme'], data['message_count']
                )
            )
            await state.update_data(text=message.text)

    else:
        await bot.delete_message(message.chat.id, message.message_id - 2)
        await bot.delete_message(message.chat.id, message.message_id - 1)
        await message.answer("🔚 Ты вышел из спам-билдера.")
        await message.answer(
            f"🥷🏻 <b>Твой профиль!</b>\n"
            f"├ 🆔<b>:</b> <code>{message.from_user.id}</code>\n"
            f"├ 💳 <b>Реквизиты:</b> <code>{get_reqs(message.from_user.id)}</code>\n"
            f"└ 🧊 <b>Баланс:</b> <code>{db.user_info(message.from_user.id)['balance']:.1f}</code>₽\n\n"
            f"📦 <b>Заказы</b>\n"
            f"├ <b>Сегодня:</b> <code>{db.count_today(message.from_user.id)}</code>\n"
            f"├ <b>За 7 дней:</b> <code>{db.count_week(message.from_user.id)}</code>\n"
            f"├ <b>За 30 дней:</b> <code>{db.count_month(message.from_user.id)}</code>\n"
            f"├ <b>Всего:</b> <code>{len(list(db.orders.find({'user_id': message.from_user.id})))}</code>\n"
            f"└ 📬 <b>Сообщений отправлено:</b> <code>{db.count_all_messages(message.from_user.id)}</code>\n\n"
            f"💥 <b>Рейтинг</b>\n"
            f"├ 🃏 <b>Статус:</b> <code>{get_rate_status(db.count_rating(message.from_user.id))}</code>\n"
            f"└ 🏆 <b>Кубков:</b> <code>{db.count_rating(message.from_user.id)}</code>\n\n"
            f"🤝 <b>Реферальная система</b>\n"
            f"├ 👥 <b>Рефералов:</b> <code>{db.count_referrals(message.from_user.id)}</code>\n"
            f"└ 💲 <b>Процент:</b> <code>{get_ref_percent(db.count_rating(message.from_user.id))}</code>%",
            reply_markup=deposit_menu(message.from_user.id)
        )
        await state.clear()


@router.callback_query(EditFactory.filter(F.action.startswith("text")))
async def text_editing(call: CallbackQuery, callback_data: EditFactory, state: FSMContext):
    data = await state.get_data()
    action = callback_data.action.split("_")[1]
    if action == "add":
        await call.message.delete()
        await call.message.answer("Введи текст:")

    elif action == "delete":
        if callback_data.media and callback_data.url:
            media = InputMedia(
                type='photo',
                media=f"{data['media']}"
            )
            await call.message.edit_media(
                media,
                reply_markup=edit_sets(
                    False,
                    True,
                    True,
                    data['spam_theme'],
                    data['message_count'],
                    data['inline']
                )
            )
        elif callback_data.media and not callback_data.url:
            media = InputMedia(
                type='photo',
                media=f"{data['media']}"
            )
            await call.message.edit_media(
                media,
                reply_markup=edit_sets(
                    False,
                    True,
                    False,
                    data['spam_theme'],
                    data['message_count']
                )
            )

        elif not callback_data.media:
            await call.message.delete()
            await call.message.answer(
                "Отправь боту то, что будет рассылаться пользователям.\n"
                "Это может быть все, что угодно - текст, фото"
            )
    await state.update_data(text="")


@router.callback_query(EditFactory.filter(F.action.startswith("media")))
async def text_editing(call: CallbackQuery, callback_data: EditFactory, state: FSMContext):
    data = await state.get_data()
    action = callback_data.action.split("_")[1]
    if action == "add":
        await call.message.edit_text("Отправь фотографию")

    elif action == "delete":
        if callback_data.text and callback_data.url:
            await call.message.delete()
            await call.message.answer(
                data['text'],
                reply_markup=edit_sets(
                    True, False, True, data['spam_theme'], data['message_count'], url_buttons=data['inline']
                )
            )
        elif callback_data.text and not callback_data.url:
            await call.message.delete()
            await call.message.answer(
                data['text'],
                reply_markup=edit_sets(True, False, False, data['spam_theme'], data['message_count'])
            )

        elif not callback_data.text:
            await call.message.delete()
            await call.message.answer(
                "Отправьте боту то, что будет рассылаться пользователям.\n"
                "Это может быть все, что угодно - текст, фото"
            )
    await state.update_data(media="")


@router.callback_query(EditFactory.filter(F.action.startswith("url")))
async def text_editing(call: CallbackQuery, callback_data: EditFactory, state: FSMContext):
    data = await state.get_data()
    action = callback_data.action.split("_")[1]
    if action == "add":
        builder = ReplyKeyboardBuilder()
        builder.button(text="Отмена")
        await call.message.delete()
        await call.message.answer(
            "Отправь мне список URL-кнопок в одном сообщении. Пожалуйста, следуйте этому формату:\n\n"
            "<code>Кнопка 1 - http://example1.com\nКнопка 2 - http://example2.com</code>",
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
        await state.set_state(UserState.inline)

    elif action == "delete":
        if callback_data.text and callback_data.media:
            await call.message.edit_reply_markup(
                reply_markup=edit_sets(True, True, False, data['spam_theme'], data['message_count'])
            )
        elif callback_data.text and not callback_data.media:
            await call.message.edit_reply_markup(
                reply_markup=edit_sets(True, False, False, data['spam_theme'], data['message_count'])
            )

        elif not callback_data.text and callback_data.media:
            await call.message.edit_reply_markup(
                reply_markup=edit_sets(False, True, False, data['spam_theme'], data['message_count'])
            )
    await state.update_data(inline="")


@router.message(UserState.inline, F.text)
async def getting_inline_buttons(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    text = await check_text(data)
    media = await check_media(data)

    await bot.delete_message(message.chat.id, message.message_id - 1)
    if message.text != "Отмена":
        links = message.text.split("\n")
        await state.update_data(inline=links)
        await message.answer("URL-кнопки добавлены.", reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(message.chat.id, message.message_id + 1)
        if media and text:
            try:
                await message.answer_photo(
                    photo=f"{data['media']}",
                    caption=f"{data['text']}",
                    reply_markup=edit_sets(
                        True, True, True, data['spam_theme'], data['message_count'], url_buttons=links
                    )
                )
                await state.set_state(UserState.client_text)
            except IndexError:
                await message.answer(
                    "Пожалуйста, следуй этому формату:\n\n"
                    "<code>Кнопка 1 - http://example1.com\n"
                    "Кнопка 2 - http://example2.com</code>"
                )

        elif media and not text:
            try:
                await message.answer_photo(
                    photo=data['media'],
                    reply_markup=edit_sets(
                        False, True, True, data['spam_theme'], data['message_count'], url_buttons=links
                    )
                )
                await state.set_state(UserState.client_text)
            except IndexError:
                await message.answer(
                    "Пожалуйста, следуй этому формату:\n\n"
                    "<code>Кнопка 1 - http://example1.com\n"
                    "Кнопка 2 - http://example2.com</code>"
                )

        elif not media and text:
            try:
                await message.answer(
                    data['text'],
                    reply_markup=edit_sets(
                        True, False, True, data['spam_theme'], data['message_count'], url_buttons=links
                    )
                )
                await state.set_state(UserState.client_text)
            except IndexError:
                await message.answer(
                    "Пожалуйста, следуй этому формату:\n\n"
                    "<code>Кнопка 1 - http://example1.com\n"
                    "Кнопка 2 - http://example2.com</code>"
                )
    else:
        await message.answer("Отмена..", reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(message.chat.id, message.message_id + 1)

        if media and text:
            await message.answer_photo(
                photo=f"{data['media']}",
                caption=f"{data['text']}",
                reply_markup=edit_sets(True, True, False, data['spam_theme'], data['message_count'])
            )
            await state.set_state(UserState.client_text)

        elif media and not text:
            await message.answer_photo(
                photo=data['media'],
                reply_markup=edit_sets(False, True, False, data['spam_theme'], data['message_count'])
            )
            await state.set_state(UserState.client_text)

        elif text and not media:
            await message.answer(
                data['text'],
                reply_markup=edit_sets(True, False, False, data['spam_theme'], data['message_count'])
            )
            await state.set_state(UserState.client_text)


@router.callback_query(F.data.startswith("spambuild"))
async def editing_buttons(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")[1]
    if action == "theme":
        await call.message.delete()
        await call.message.answer(
            "🌚 Выбери целевую аудиторию.",
            reply_markup=choose_theme()
        )
    elif action == "count":
        await call.message.delete()
        await call.message.answer(
            "🔢 Выбери количество сообщений.\n\n"
            f"<i>1 сообщение = <code>{get_price(db.count_rating(call.from_user.id))}</code>₽</i>",
            reply_markup=choose_count()
        )
        await state.set_state(UserState.message_count)


@router.callback_query(EditFactory.filter(F.action == "finish"))
async def setup_complete(call: CallbackQuery, state: FSMContext, callback_data: EditFactory, bot: Bot):
    data = await state.get_data()

    if db.user_info(call.from_user.id)['balance'] >= (data['message_count'] * get_price(db.count_rating(call.from_user.id))):
        number = random.randint(0, 9999)
        db.create_spam_order(number, call.from_user.id, data['message_count'], data['spam_theme'])
        db.update_string(
            call.from_user.id,
            {'balance': (db.user_info(call.from_user.id)['balance'] - (data['message_count'] * db.get_current_price()))}
        )

        if callback_data.text and callback_data.media and callback_data.url:
            media = InputMedia(
                type="photo",
                media=f"{data['media']}",
                caption=f"{data['text']}\n"
                        f"-----------------------------------\n"
                        f"<b>#{number}\n\n</b>"
                        f"Аудитория: {data['spam_theme']}\n"
                        f"Кол-во сообщений: {data['message_count']}\n\n"
                        f"<i>♻️ Бот отправит тебе сообщение, когда начнется рассылка</i>\n"

            )
            await call.message.edit_media(
                media,
                reply_markup=client_finish_buttons(data['inline'])
            )
            await bot.send_photo(
                chat_id=6364771832,
                photo=data['media'],
                caption=f"{data['text']}\n"
                        f"-----------------------------------\n"
                        f"<b>#{number}\n\n</b>"
                        f"Аудитория: {data['spam_theme']}\n"
                        f"Кол-во сообщений: {data['message_count']}\n\n"
                        f"message_id: <code>{call.message.message_id + 2}</code>",
                reply_markup=admin_spam_start(
                    call.from_user.id,
                    number,
                    data['inline'])
            )

        elif callback_data.text and callback_data.media and not callback_data.url:
            media = InputMedia(
                type="photo",
                media=f"{data['media']}",
                caption=f"{data['text']}\n"
                        f"-----------------------------------\n"
                        f"<b>#{number}\n\n</b>"
                        f"Аудитория: {data['spam_theme']}\n"
                        f"Кол-во сообщений: {data['message_count']}\n\n"
                        f"<i>♻️ Бот отправит тебе сообщение, когда начнется рассылка</i>\n"
            )
            await call.message.edit_media(media)
            await bot.send_photo(
                chat_id=6364771832,
                photo=data['media'],
                caption=f"{data['text']}\n"
                        f"-----------------------------------\n"
                        f"<b>#{number}\n\n</b>"
                        f"Аудитория: {data['spam_theme']}\n"
                        f"Кол-во сообщений: {data['message_count']}\n\n"
                        f"message_id: <code>{call.message.message_id + 2}</code>",
                reply_markup=admin_spam_start(
                    call.from_user.id,
                    number
                )
            )

        elif callback_data.text and callback_data.url and not callback_data.media:
            await call.message.edit_text(
                f"{data['text']}\n"
                f"-----------------------------------\n"
                f"<b>#{number}\n\n</b>"
                f"Аудитория: {data['spam_theme']}\n"
                f"Кол-во сообщений: {data['message_count']}\n\n"
                f"<i>♻️ Бот отправит тебе сообщение, когда начнется рассылка</i>\n",
                reply_markup=client_finish_buttons(data['inline'])
            )
            await bot.send_message(
                6364771832,
                f"{data['text']}\n"
                f"-----------------------------------\n"
                f"<b>#{number}\n\n</b>"
                f"Аудитория: {data['spam_theme']}\n"
                f"Кол-во сообщений: {data['message_count']}\n\n"
                f"message_id: <code>{call.message.message_id + 2}</code>",
                reply_markup=admin_spam_start(
                    call.from_user.id,
                    number,
                    data['inline'])
            )

        elif callback_data.media and callback_data.url and not callback_data.text:
            media = InputMedia(
                type="photo",
                media=f"{data['media']}",
                caption=f"<b>#{number}\n\n</b>"
                        f"Аудитория: {data['spam_theme']}\n"
                        f"Кол-во сообщений: {data['message_count']}\n\n"
                        f"<i>♻️ Бот отправит тебе сообщение, когда начнется рассылка</i>\n"
            )
            await call.message.edit_media(media, reply_markup=data['inline'])
            await bot.send_photo(
                chat_id=6364771832,
                photo=data['media'],
                caption=f"<b>#{number}\n\n</b>"
                        f"Аудитория: {data['spam_theme']}\n"
                        f"Кол-во сообщений: {data['message_count']}\n\n"
                        f"message_id: <code>{call.message.message_id + 2}</code>",
                reply_markup=admin_spam_start(
                    call.from_user.id,
                    number,
                    data['inline'])
            )

        elif callback_data.media and not callback_data.text and not callback_data.url:
            media = InputMedia(
                type="photo",
                media=f"{data['media']}",
                caption=f"<b>#{number}\n\n</b>"
                        f"Аудитория: {data['spam_theme']}\n"
                        f"Кол-во сообщений: {data['message_count']}\n\n"
                        f"<i>♻️ Бот отправит тебе сообщение, когда начнется рассылка</i>\n"
            )
            await call.message.edit_media(media)
            await bot.send_photo(
                chat_id=6364771832,
                photo=data['media'],
                caption=f"<b>#{number}\n\n</b>"
                        f"Аудитория: {data['spam_theme']}\n"
                        f"Кол-во сообщений: {data['message_count']}\n\n"
                        f"message_id: <code>{call.message.message_id + 2}</code>",
                reply_markup=admin_spam_start(
                    call.from_user.id,
                    number
                )
            )

        elif callback_data.text and not callback_data.media and not callback_data.url:
            await call.message.edit_text(
                f"{data['text']}\n"
                f"-----------------------------------\n"
                f"<b>#{number}\n\n</b>"
                f"Аудитория: {data['spam_theme']}\n"
                f"Кол-во сообщений: {data['message_count']}\n\n"
                f"<i>♻️ Бот отправит тебе сообщение, когда начнется рассылка</i>\n"
            )
            await bot.send_message(
                6364771832,
                f"{data['text']}\n"
                f"-----------------------------------\n"
                f"<b>#{number}\n\n</b>"
                f"Аудитория: {data['spam_theme']}\n"
                f"Кол-во сообщений: {data['message_count']}\n\n"
                f"message_id: <code>{call.message.message_id + 2}</code>",
                reply_markup=admin_spam_start(
                    call.from_user.id,
                    number
                )
            )

        await state.clear()

    else:
        await call.message.answer(
            f"📛 На твоем счету недостаточно средств.\n\n"
            f"Пополни баланс - /profile или измени количество сообщений."
        )


@router.callback_query(F.data == "exitFromBuilder")
async def exiting_from_builder(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        "🔚 Ты вышел из спам-билдера.\n\n"
        '<i>Чтобы воспользоваться функциями <b>SpamShark</b> еще раз, нажми кнопку <b>"Меню"</b></i>\n\n'
    )
    await state.clear()


@router.callback_query(F.data.startswith("startspam"))
async def starting_spam(call: CallbackQuery, bot: Bot):
    user_id = int(call.data.split("_")[1])
    order_id = int(call.data.split("_")[2])
    order = db.get_order_info(order_id)
    await call.message.edit_reply_markup(reply_markup=admin_spam_end())

    await bot.send_message(
        user_id,
        f"<b>#{order_id}\n\n</b>"
        f"Аудитория: {order['theme']}\n"
        f"Кол-во сообщений: {order['messages']}\n\n"
        f"📬 Идет спам-рассылка.. 0%"
    )


@router.callback_query(F.data == "endSpam")
async def end_spamming(call: CallbackQuery):
    await call.message.delete()
