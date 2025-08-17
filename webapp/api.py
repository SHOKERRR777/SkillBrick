import os
import aiofiles

import httpx

import uvicorn     
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from bitrix import create_request_to_bitrix, get_chat_from_bitrix, get_video_from_bitrix

import Database.request as rq
from Database.models import User, Course, Request_user, async_session

templates = Jinja2Templates(directory="webapp/templates")

# Добавляем таблицы БД в этот файл
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session as session:
        print("Bot is ready")
        yield

app = FastAPI("To do app", lifespan=lifespan)

@app.get('/', response_class=HTMLResponse)
async def video_from_course(request: Request):
    tg_id = request.query_params.get("tg_id")

    if not tg_id:
        return "Пользователь не был найден!", 403
     
    user_list = await rq.user_info(tg_id=int(tg_id)) 
    video_url = await get_video_from_bitrix(file_id=('1234')) # file_id - айди на видео

    return templates.TemplateResponse('videocourse.html', user_list=user_list, video_url=video_url)

# Запуск нашего бота
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)