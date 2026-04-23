from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.account_auth.dependencies import auth
from app.modules.account_auth.models import User
from .schemas import MessageCreate, MessageResponse
from .services import create_message, get_all_messages, get_messages_by_user, search_messages_by_word, delete_message

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/messages", response_model=MessageResponse)
async def post_message(
    message: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth)
):
    return await create_message(db, message, current_user.username)

@router.get("/messages", response_model=list[MessageResponse])
async def get_messages(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth)
):
    return await get_all_messages(db, limit, offset)

@router.get("/messages/{username}", response_model=list[MessageResponse])
async def get_user_messages(
    username: str,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth)
):
    return await get_messages_by_user(db, username, limit, offset)

@router.get("/messages/search", response_model=list[MessageResponse])
async def search_messages(
    word: str = Query(..., min_length=1),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth)
):
    return await search_messages_by_word(db, word, limit, offset)

@router.delete("/messages/delete/{message_id}", status_code=204)
async def delete(
    message_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth)
):
    success = await delete_message(db, message_id, current_user)
    
    if success == "not found":
        raise HTTPException(status_code=404, detail="Message not found")
    elif success == "forbidden":
        raise HTTPException(status_code=403, detail="You do not have permission to delete this message")
    