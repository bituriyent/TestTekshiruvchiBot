from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Testni Tekshirish'),
            KeyboardButton(text='Test Yaratish')
        ]
    ], resize_keyboard=True,
    one_time_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ortga')
        ]
    ], resize_keyboard=True,
    one_time_keyboard=True
)

testing = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Test Tuzish'),
            KeyboardButton(text='Testni O\'chirish'),
        ]
    ], resize_keyboard=True,
    one_time_keyboard=True
)
