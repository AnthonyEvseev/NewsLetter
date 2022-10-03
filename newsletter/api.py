from fastapi import APIRouter, HTTPException, status, Response, Depends
from core.database import session, connect_db
from newsletter.crud import get_history, create_history
from newsletter.schemas import NewsLetter

newsletter_router = APIRouter()


@newsletter_router.get('/newsletter', summary="Newsletter history")
async def get_newsletter(db: session = Depends(connect_db)):
    return get_history(db)


@newsletter_router.post('/newsletter', summary="Create a newsletter")
async def post_newsletter(schemas: NewsLetter, response: Response, db: session = Depends(connect_db)):
    try:
        create_history(schemas, db)
        response.status_code = status.HTTP_200_OK
        return 'post работает'
    except:
        raise HTTPException(status_code=400, detail='')


@newsletter_router.put('/newsletter', summary="Put information about newsletters")
async def put_newsletter(schemas: NewsLetter, response: Response, db: session = Depends(connect_db)):
    return 'put работает'


@newsletter_router.delete('/newsletter', summary="Delete information about newsletters")
async def delete_newsletter(schemas: NewsLetter, response: Response, db: session = Depends(connect_db)):
    return 'delete работает'
