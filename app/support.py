from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from create_bot import bot

help_router = Router()

# Специальный класс для машины состояния, чтобы бот знал, что сейчас пользователь задаёт вопрос в поддержку, а не просто спамит
class User_answer(StatesGroup):
    name = State()
    message = State()


@help_router.message(F.text == "Написать в поддержку")
async def user_answer_first(message: Message, state: FSMContext):
    await state.set_state(User_answer.name)
    await message.answer("Для начала напишите Ваше имя")

@help_router.message(User_answer.name)
async def user_answer_second(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(User_answer.message)
    await message.answer("Задавайте Ваш вопрос")

@help_router.message(User_answer.message)
async def user_answer_third(message: Message, state: FSMContext):
    await state.update_data(message=message.text)
    await state.set_state(User_answer.message)
    await message.answer("Ваш вопрос был передан в поддержку!")
    
    data = await state.get_data() # Здесь сохраняется вся информация от пользователя, полученная с машины состояния

    text_to_support = f"Имя пользователя: {data['name']}, \nВопрос в поддержку: {data['message']}"

    # Пересылаем вопрос от пользователя в указанный чат
    await bot.send_message(
        chat_id=1704827815,
        text = text_to_support
    )

    await state.clear() # Очищаем машину состояний, чтобы не засорять оперативку