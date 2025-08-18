import time

from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

import config
from create_bot import bot

import Database.request as rq

router_payments = Router()

PRICE = [LabeledPrice(label="Оплата подписки для закрытого тгк канала", amount=50000)] # amount в копейках, т.е сейчас 1 рубль

""" Обработчик команды 'Оплатить подписку' """
@router_payments.message(F.text == "Оплатить подписку")
@router_payments.message(Command("payments"))
async def pay_sub(message: Message):
    await bot.send_invoice(chat_id=message.chat.id, 
                           title="Оплата подписки для закрытого тгк канала", 
                           description="Помимо закрытого тгк канала откроется доступ к Web-приложению", 
                           payload='invoice', 
                           provider_token=config.PROVIDER_TOKEN, 
                           prices=PRICE,
                           currency='rub', 
                           start_parameter="subscription")
    
""" Обязательный ответ на PreCheckoutQuery """
@router_payments.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

""" Обработчик успешной оплаты """
@router_payments.message(F.successful_payment)
async def successful_payment(message: Message):
    await rq.is_paid(message.from_user.id)
    
    # Генерируем ссылку, которая будет действительна в течение 10 минут
    invite_link = await bot.create_chat_invite_link(
        chat_id=config.CLOSED_TGK,
        member_limit=1,
        expire_date=int(time.time()) + 600)    
    
    await message.answer(f"""
✅ Оплата успешно завершена!

🔗 Ссылка на закрытый ТГ-канал:
{invite_link.invite_link}

⚠️ Внимание! Ссылка действительна только 10 минут. Если вы не успели перейти, запросите новую, используя команду:
/getlink
""")
    
""" Обработчик команды 'getlink' """
@router_payments.message(Command('getlink'))
async def new_link(message: Message):
    user = await rq.user_info(tg_id=message.from_user.id)

    if user['is_paid'] == False:
        await bot.answer("Ваша подписка не действительна! Для ее активации воспользуйтесь командой /payments")

    # Генерируем ссылку, которая будет действительна в течение 10 минут
    invite_link = await bot.create_chat_invite_link(
        chat_id=config.CLOSED_TGK,
        member_limit=1,
        expire_date=int(time.time()) + 600)    

    await message.answer(f"""
🔐 Новая ссылка на закрытый ТГ-канал

Ваш уникальный доступ:
{invite_link.invite_link}

⏳ Срок действия: 10 минут
⚠️ Ссылка автоматически деактивируется через указанное время
""")    