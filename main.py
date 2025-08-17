import asyncio

from app.users_panel import user_router
from app.admin import admin_router
from app.payments import router_payments
from app.support import help_router

from Database.models import async_main
from create_bot import bot, dp, admins

""" Функция, которая выполняется, когда бот запускается """
async def start_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, "Я запущен, вы находитесь в админ-панеле")
    except:
        pass

""" Функция, которая выполняется, когда бот отключается """
async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, "Бот был остановлен!")
    except:
        pass

""" Асинхронная функция для запуска модулей """
async def main():
    # Подключаем роутеры
    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(router_payments)
    dp.include_router(help_router)

    # Подключаем start_bot и stop_bot
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Запуск бота в режиме long polling при запуске бот очищает все обновления, которые были за его моменты бездействия
    try:
        await async_main()
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except:
        bot.session.close()

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())