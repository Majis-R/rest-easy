from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from .models import Message
from .schemas import MessageCreate
from app.modules.account_auth.models import User

async def create_message(db: AsyncSession, message: MessageCreate, sender_username: str) -> Message:
    db_message = Message(sender_username=sender_username, content=message.content)
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message

async def get_all_messages(db: AsyncSession, limit: int = 100, offset: int = 0) -> list[Message]:
    result = await db.execute(select(Message).order_by(Message.timestamp.desc()).limit(limit).offset(offset))
    return list(result.scalars().all())

async def get_messages_by_user(db: AsyncSession, username: str, limit: int = 100, offset: int = 0) -> list[Message]:
    result = await db.execute(
        select(Message).where(Message.sender_username == username).order_by(Message.timestamp.desc()).limit(limit).offset(offset)
    )
    return list(result.scalars().all())

async def search_messages_by_word(db: AsyncSession, word: str, limit: int = 100, offset: int = 0) -> list[Message]:
    result = await db.execute(
        select(Message).where(Message.content.ilike(f"%{word}%")).order_by(Message.timestamp.desc()).limit(limit).offset(offset)
    )
    return list(result.scalars().all())

async def delete_message(db: AsyncSession, message_id: int, user: User) -> bool:
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    
    if not message:
        return "not found"
    
    if message.sender_username != user.username and user.role != "admin":
        return "forbidden"
    
    await db.delete(message)
    await db.commit()
    return "success"