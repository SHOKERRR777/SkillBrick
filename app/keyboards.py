from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мой профиль")],
    [KeyboardButton(text="Панель администратора")],
    [KeyboardButton(text="Поддержка")],
], resize_keyboard=True)

webapp_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Открыть видео с курса",
        web_app=WebAppInfo(url="None")
                          )],
])

support_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Написать в поддержку")]
], resize_keyboard=True)

info_about_users = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Посмотреть информацию о пользователе")]
], resize_keyboard=True)

user_actions = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Удалить пользователя")],
    [KeyboardButton(text="Выйти")]
])

async def delete_user_kb():
    delete_user = InlineKeyboardBuilder()
    delete_user.add(
        InlineKeyboardButton(
            text="Да",
            callback_data="delete_yes"
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data="delete_no"
        )
    )