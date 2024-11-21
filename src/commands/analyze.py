import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.config import config
from src.services.openai.service import OpenAIClient
from src.services.thought_analysis import AnalysisService
from src.states.thought_analysis_states import ThoughtAnalysis

logger = logging.getLogger('bot.commands.analyze')


router = Router()

ALLOWED_USER_IDS = config.ALLOWED_IDS
openai_client = OpenAIClient(config.OPENAI_API_KEY.get_secret_value())
analysis = AnalysisService(openai_client)

@router.message(Command('analyze'),F.from_user.id.in_(ALLOWED_USER_IDS))
async def start_analysis(message: Message, state: FSMContext):
    await state.set_state(ThoughtAnalysis.enter_thought)
    await message.answer("Введите вашу мысль, которую хотите проанализировать.")

@router.message(ThoughtAnalysis.enter_thought)
async def process_enter_thought(message: Message, state: FSMContext):
    """
    Обработчик для получения и проверки мысли от пользователя.
    """
    thought = message.text
    data = await state.get_data()
    attempts = data.get("attempts", 0)

    # Проверка на то, что текст похож на "мысль" (можно заменить на более сложный алгоритм)
    if analysis.is_valid_thought(thought):
        await state.update_data(thought=thought)
        await state.set_state(ThoughtAnalysis.analyze_thought)
        await message.answer(
            "Анализирую вашу мысль на наличие когнитивных искажений. Пожалуйста, подождите..."
        )

        # Вызов функции для анализа мысли

        cognitive_distortions = analysis.analyze_all_distortions(thought)
        await state.update_data(distortions=cognitive_distortions)

        distortions_to_focus_on = analysis.suggest_focus_distortions(thought, cognitive_distortions)

        await state.update_data(distortions_to_focus_on=distortions_to_focus_on)

        # Формируем сообщение с подробностями
        distortion_messages = []
        for result in cognitive_distortions:
            for name, schema_result in result.items():
                try:
                    presence = f"Присутствие искажения: {'Да' if schema_result.present else 'Нет'}"
                    reasoning = f"Обоснование: {schema_result.reasoning}"
                    distortion_messages.append(f"{name}:\n{presence}\n{reasoning}\n")
                except AttributeError:
                    # Пропускаем, если в результате отсутствует одно из полей
                    pass

        # Соединяем все сообщения в одно
        full_message = "Мы обнаружили следующие когнитивные искажения:\n\n" + "\n".join(
            distortion_messages
        )

        # Переход к следующему состоянию
        await state.set_state(ThoughtAnalysis.provide_rational_response)
        # Отправляем сообщение пользователю
        await message.answer(full_message)

        await message.answer('============')

        focus_text = "\n".join(
        f"{distortion.name}: {distortion.reason}" 
        for distortion in distortions_to_focus_on.selected_distortions
        )   

        await message.answer(focus_text)

        await message.answer('============')

        await message.answer(
            "Теперь давайте попробуем сформулировать более рациональный ответ."
        )
    else:
        # Увеличиваем счётчик попыток
        attempts += 1
        await state.update_data(attempts=attempts)

        if attempts >= 3:
            # Если три попытки неудачны, завершить процесс
            await state.clear()
            await message.answer(
                "Извините, но я не смог распознать вашу мысль. Попробуйте начать процесс заново."
            )
        else:
            # Запросить повторный ввод
            await message.answer(
                "Это не похоже на мысль. Попробуйте снова. Пожалуйста, сформулируйте вашу мысль более конкретно."
            )



# Обработчик для формулирования рационального ответа
@router.message(ThoughtAnalysis.provide_rational_response)
async def formulate_rational_response(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    user_thought = data['thought']
    selected_distortions = data['distortions_to_focus_on']
    
    if not user_thought or not selected_distortions:
        await message.answer("Не удалось найти данные для анализа. Попробуйте начать заново.")
        await state.clear()
        return

    # Тут происходит обращение в ГПТ
    rational_response = analysis.generate_rational_response(user_thought, selected_distortions)
    await state.update_data(rational_response=rational_response)

    additional_comments = rational_response.additional_comments
    rational_response = rational_response.rational_response

    logger.debug(rational_response)
    logger.debug(additional_comments)


    await message.answer(
        f"Вот рациональный ответ на вашу мысль:\n\n{rational_response}\n\n"
        f"Дополнительные комментарии:\n\n{additional_comments}\n\n"
        "Помогло ли это вам почувствовать себя лучше?"
    )
    await state.clear()
