import logging

aiogram_logger = logging.getLogger("aiogram")
aiogram_logger.setLevel(logging.INFO)

# Создание обработчика для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Формат сообщений
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Добавляем обработчик только к aiogram логгеру
aiogram_logger.addHandler(console_handler)

def setup_logger(name, level=logging.DEBUG):

    # Создаем логгер с заданным именем
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Создаем форматтер для вывода
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Создаем консольный хендлер и добавляем его к логгеру
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
