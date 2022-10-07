from fastapi import APIRouter, Depends, Query
from core.config import SECRET_TOKEN
from core.database import session, connect_db
from newsletter.newsletter import send_messages

newsletter_router = APIRouter()

header = {'Authorization': SECRET_TOKEN}


@newsletter_router.get('/test', summary="test")
async def test(text: str, tag: str, code: str = Query(max_length=3), db: session = Depends(connect_db)):
    return send_messages(text, tag, code, db)
