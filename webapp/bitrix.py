import os
import httpx

BITRIX_WEBHOOK = os.getenv("BITWIX_WEBHOOK", 
"ССЫЛКА НА BITRIX")

""" Функция, с помощью которой запрос от пользователя отправляется в BitRix """
async def create_request_to_bitrix(user_id: int, message: str):
    """ Создание обращения в BitRix """
    async with httpx.AsyncClient() as client:
        payload = {
            "FIELDS" : {
                "TITLE" : f"Обращение от пользователя {user_id}",
                "COMMENTS" : message,
                "ASSIGNED_BY_ID" : 1 # Айди админа в BitRix
            }
        }

        r = await client.post(f"{BITRIX_WEBHOOK}crm.lead.add.json", data=payload) # Обращение от пользователя делаем в виде Json-файла

        return r.json()

""" Функция, с помощью которой сообщения с BitRix пересылаются в tg """ 
async def get_chat_from_bitrix():
    """ Получение данных из BitRix """
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BITRIX_WEBHOOK}crm.lead.list.json", params={"select[]" : ["ID", "TITLE"]}) # Получаем с BitRix сообщения определённого пользователя

        return r
    
""" Функция, с которой пользователь в WebApp получает видеоурок с курса """
async def get_video_from_bitrix(file_id: str):
    """ Получение видеоурока с BitRix """
    async with httpx.AsyncClien() as client:
        with open("file", r) as f:
            r = await client.get(f"{BITRIX_WEBHOOK}disk.file.get", params={"id" : file_id}) # Вместо единички айди папки в BitRix 

            file_info = r.json()

            return file_info["result"] ["DOWNLOAD_URL"]