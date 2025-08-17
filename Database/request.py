from aiogram.types import Message

from Database.models import async_session, User, Course, Request_user
from sqlalchemy import select

from config import ADMINS_ID

""" Функция, добовляющая пользователя в БД или позволяет пользователю зайти в свой профиль"""
async def set_user(tg_id: int, username: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id, User.username == username))

        if not user:
            new_user = User(tg_id=tg_id, username=username)
            session.add(new_user)
            await session.commit()
            return new_user
        # Если найден пользователь, но он поменял какие-то данные (имя)
        else:
            if username and user.username != username:
                user.username = username
                await session.commit
            
            return user

""" Функция, выводящая всю информацию о пользователе """
async def user_info(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        # Если пользователь без тг айди
        if not tg_id:
            return "Произошла ошибка, не можем определить ваше айди!"

        # Возвращаем словарь с данными о пользователе
        return {
            "id" : user.id,
            "tg_id" : user.tg_id,
            "username" : user.username,
            "created_time" : user.created_time,
            "is_paid" : user.is_paid,
        }

""" Функция, которая проверяет, заплатил ли пользователь за подписку """   
async def is_paid(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return "Произошла ошибка! Пользователь не был найден!"
        
        # Меняем значение is_paid на True, если пользователь заплатил за подписку
        user.is_paid = True
        await session.commit()

""" Функция, с помощью которой админ может найти профиль по имени """
async def search_user(username: str):
    async with async_session() as session:
        user_intable = await session.scalar(select(User).where(User.username == username))

        if not user_intable:
            return "Просим прощения, пользователь с таким именем не был найден! Повторите попытку"
        
        return {
            'id' : user_intable.id,
            'tg_id' : user_intable.tg_id,
            'username' : user_intable.username,
            'created_time' : user_intable.createdtime,
            'is_paid' : user_intable.is_paid
        }
    
""" Функия, с помощью которой админ может удалить пользователя из Базы Данных """
async def delete_user(username: str):
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        if not user:
            return False

        await session.delete(user)
        await session.commit()

        return True