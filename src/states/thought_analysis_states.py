from aiogram.fsm.state import State, StatesGroup


# Определяем состояния с помощью StatesGroup
class ThoughtAnalysis(StatesGroup):
    enter_thought = State()  # Ожидание ввода мысли от пользователя
    # Здесь же какая-то проверка, что это мысль или типа того
    analyze_thought = State()  # Анализ на когнитивные искажения
    provide_rational_response = State()  # Формулирование рационального ответа
