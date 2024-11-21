import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.commands.analyze import start_analysis

logger = logging.getLogger('bot.commands.start')

router = Router()

# Создание инлайн-клавиатуры с подбробным описанием бота
detailed_description_kb = InlineKeyboardBuilder()
detailed_description_kb.button(text="Что такое когнитивные искажения?", callback_data="what_is_cognitive_distortions")
detailed_description_kb.button(text="Зачем тренироваться их идентифицировать и формулировать рациональный ответ?", callback_data="why_train")
detailed_description_kb.button(text="Как все это работает?", callback_data="how_it_works")
detailed_description_kb.button(text="Я все знаю, перейдем к тренировке", callback_data="start_training")
detailed_description_kb.adjust(1)  # Каждая кнопка на отдельной строке

# Создание инлайн-клавиатуры
inline_kb = InlineKeyboardBuilder()
inline_kb.button(text="О боте", callback_data="about")
inline_kb.button(text="О боте 2", callback_data="about2")
inline_kb.button(text="Начать процесс", callback_data="start_process")
inline_kb.adjust(2, 1)  # Устанавливаем количество кнопок в строках

@router.message(CommandStart())
async def description(message: Message, is_new_user: bool):

    # if is_new_user:
    if True:
        # Сообщение для нового пользователя
        welcome_message = (
            "Я бот для тренировки идентификации когнитивных искажений в мышлении и формулирования рационального ответа.\n\n"
            "Что я делаю:\n"
            "- Помогаю выявить когнитивные искажения.\n"
            "- Учусь составлять обоснованные, рациональные ответы.\n\n"
            "**Дисклеймер:** Это не терапия, а вспомогательный инструмент.\n"
            "Если вам совсем плохо, обратитесь за помощью к квалифицированному специалисту.\n\n"
            "Начнем с теории или сразу перейдем к практике?"
        )
        await message.answer(welcome_message, reply_markup=detailed_description_kb.as_markup())
    else:
        await message.answer('Рад видеть вас снова!')
        await message.answer(
            "Описание",
            reply_markup=inline_kb.as_markup(),
        )

@router.callback_query()
async def handle_callback(callback_query: CallbackQuery, state):
    data = callback_query.data
    if data == "what_is_cognitive_distortions":
        await callback_query.message.answer("Когнитивные искажения — это систематические ошибки в мышлении, которые искажают восприятие реальности.")
    elif data == "why_train":
        await callback_query.message.answer("Тренировка помогает развивать навыки критического мышления и рационального анализа.")
    elif data == "how_it_works":
        await callback_query.message.answer("Я предложу ситуации с когнитивными искажениями, а вы попробуете найти их и предложить рациональный ответ.")
    elif data == "start_training":
        await callback_query.message.answer("Отлично! Переходим к тренировке.")
        await start_analysis(callback_query.message, state)
    elif data == "about":
        await callback_query.message.answer("Информация о боте.")
    elif data == "about2":
        await callback_query.message.answer("Дополнительная информация о боте.")
    elif data == "start_process":
        await start_analysis(callback_query.message, state)

    await callback_query.answer()  # Закрываем уведомление о нажатии

