from sqlalchemy import BigInteger, Boolean, DateTime, String, ForeignKey

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

engine = create_async_engine(url='sqlite+aiosqlite:///dp.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

""" Таблица пользователей """
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(25))
    created_time = mapped_column(DateTime, server_default=func.now())
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)

""" Таблица для 'Курсы и видео' """
class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(150))
    video_url: Mapped[str] = mapped_column(String(100))

""" Таблица для обращения и заявок, если Bitrix будет не исправен """
class Request_user(Base):
    __tablename__ = 'requestusers'

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String(500))
    id_user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    send_time = mapped_column(DateTime, server_default=func.now())

""" Функция для запуска таблиц бд в main.py """
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)   