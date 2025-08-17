from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import F, Router, types
from aiogram.filters.command import Command

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

from create_bot import admins
from config import ADMINS_ID

import Database.request as rq

admin_router = Router()

# Класс для машины состояния для поиска пользователя по имени
class Search_user(StatesGroup):
    username = State()
    username_to_delete = State()


@admin_router.message(F.text == 'Панель администратора')
async def admin_panel(message: Message):
    if F.from_user.id not in ADMINS_ID:
        await message.answer("Вход запрещён!")
    
    await message.answer("Добро пожаловать в админ панель!", reply_markup=kb.info_about_users)



""" Обработчик команды 'Посмотреть информацию о пользователе' """

@admin_router.message(F.text == "Посмотреть информацию о пользователе")
async def searching_user(message: Message, state: FSMContext):
    if F.from_user.id not in ADMINS_ID:
        await message.answer("Вход запрещён!")
    
    await state.set_state(Search_user.username)
    await message.answer("Введите имя пользователя, информацию о котором Вы хотите узнать", reply_markup=ReplyKeyboardRemove())

@admin_router.message(Search_user.username)
async def searching_user2(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    
    user_list = await rq.search_user(username=message.text)

    if isinstance(user_list, str):
        await message.answer(user_list)
        return

    if not user_list['is_paid']:
        await message.answer(f"""
Информация о профиле {user_list['username']}:

    ID в таблице БД: {user_list['id']}
    Телеграм ID: {user_list['tg_id']}
    Дата создания пользователя в БД: {user_list['created_time']}
    Есть ли подписка у пользователя: Нет""", reply_markup=kb.user_actions)
    else:
        await message.answer(f"""
Информация о профиле {user_list['username']}:

    ID в таблице БД: {user_list['id']}
    Телеграм ID: {user_list['tg_id']}
    Дата создания пользователя в БД: {user_list['created_time']}
    Есть ли подписка у пользователя: Да""", reply_markup=kb.user_actions)



""" Обработчик команды 'Удалить пользователя' """    

@admin_router.callback_query(F.data.starswith("delete:"))
async def confirm_delete(callback: types.CallbackQuery, state: FSMContext):
    username = callback.data.split(":")[1]

    await state.update_data(username_to_delete=username)

    await callback.message.answer(f"Вы точно хотите удалить {username} из Базы Данных?", reply_markup=kb.delete_user_kb())


""" Да/нет """
@admin_router.callback_query(F.data.in_(["delete_yes", "delete_no"]))
async def finish_delete(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    username = data.get("username_to_delete")

    if callback.data == "delete_no":
        await callback.message.answer(f"Отмена удаления пользователя {username} из таблицы Базы Данных!")
        await state.clear()
        return
    
    result = rq.delete_user(username)
    if result:
        await callback.message.answer(f"Пользователь {username} был удалён и таблицы Базы Данных!")
    else:
        await callback.message.answer(f"Пользователь с именем {username} не был найден в таблице Базы Данных!")

    await state.clear()
    await callback.answer()



""" Обработчик команды 'Выйти' """

@admin_router.message(F.text == "Выйти")
async def exit_from_func(message: Message, state: FSMContext):
    await message.answer("Вы вышли из данной команды!")
    await state.clear()