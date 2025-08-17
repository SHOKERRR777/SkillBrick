from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters.command import Command, CommandStart

from create_bot import admins

import app.keyboards as kb

import Database.request as rq

user_router = Router()


""" Обработчик команды start """
@user_router.message(CommandStart())
@user_router.message(Command('menu'))
async def start_com(message: Message):
    await rq.set_user(tg_id=message.from_user.id, username=message.from_user.username)
    await message.answer(f"""
🌟 Добро пожаловать, <b>{message.from_user.first_name}</b>!

Чтобы получить доступ к эксклюзивному закрытому ТГ-каналу, необходимо оформить подписку за 5 рублей.
Что даёт подписка?

✅ Доступ к закрытому ТГК с уникальными материалами и "плюшками"
✅ Мини-приложение с курсами и обучающими видео по устройству автомобилей
Как оплатить?

    Воспользуйтесь командой /payments

    Следуйте инструкциям платежной системы

    После подтверждения оплаты вы автоматически получите доступ

💡 Ссылка на канал придет сразу после оплаты и будет активна 10 минут. Если не успели — запросите новую через /getlink
""", reply_markup=kb.main_menu)
    

""" Обработчик команды 'Мой профиль' """
@user_router.message(F.text == "Мой профиль")
@user_router.message(Command('my_profile'))
async def my_profile(message: Message):
    user_info = await rq.user_info(tg_id=message.from_user.id) # Переменная, в которой храниться список информации о нашем пользователе
    
    # Для того, чтобы в красивом виде выводилось user_info['is_paid']
    if user_info['is_paid'] == False:
        await message.answer(f"""
Информация по вашему профилю:
    
    Имя - {user_info['username']}.
    Аккаунт зарегистрирован в боте с - {user_info['created_time']}.
    Подписка для закрытого тгк - Отсутствует.

Если вы хотите подключить подписку, то воспользуйтесь командой /start
""", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f"""
Информация по вашему профилю:
    
    Имя - {user_info['username']}.
    Аккаунт зарегистрирован в боте с - {user_info['created_time']}.
    Подписка для закрытого тгк - Активна.

Ваша подписка на данный момент!
""", reply_markup=ReplyKeyboardRemove())


""" Обработчик команды 'Поддержка' """
@user_router.message(F.text == "Поддержка")
@user_router.message(Command('help'))
async def helper(message: Message):
    await message.answer("""
🛎️ Нужна помощь?

Не стесняйся обращаться к нашему менеджеру! Он с радостью ответит на все твои вопросы и поможет с подпиской. 💬

👉 Напиши сюда: @Zakazforkwork1_Support

Мы на связи 24/7 и сделаем всё, чтобы твой опыт был идеальным! 🌟

""", reply_markup=kb.support_button)
    
""" Обработчик команды 'WebApp' """
@user_router.message(Command('WebApp'))
async def WebApp_menu(message: Message):
    user = await rq.user_info(tg_id=message.from_user.id)

    if not user or user.get("is_paid") == False:
        await message.answer("""
🔒 Доступ закрыт!

Извините, <b>{message.from_user.first_name}</b>, но эта функция доступна только подписчикам SkillBrick.

Как получить доступ?

1️⃣ Введите команду /payments
2️⃣ Оплатите подписку всего 5 рублей
3️⃣ Мгновенно получите полный доступ ко всем материалам
Ваши выгоды после оплаты:

✅ Просмотр всех видеоуроков по мостостроению
✅ Доступ к закрытому сообществу
✅ Возможность задавать вопросы экспертам

Не упустите шанс стать профессионалом!
""")
    
    await message.answer("Выберите ниже из списка нужное для Вас WebApp-приложение", reply_markup=kb.webapp_menu)