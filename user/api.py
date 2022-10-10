from fastapi import APIRouter, HTTPException, status, Response, Depends
from user.schemas import UserSchemas
from core.database import session, connect_db
from user.crud import create_user, get_user, update_user, remove_book

user_router = APIRouter()


@user_router.get('/user', summary="Get user information")
async def get_users(response: Response, db: session = Depends(connect_db)):
    """
        Инструкция:
        - После выполнения запроса будет выведен список всех доступных клиентов
    """
    response.status_code = status.HTTP_200_OK
    return 'Список клиентов', get_user(db)


@user_router.post('/user', summary="Create an user")
async def post_user(schemas: UserSchemas, response: Response, db: session = Depends(connect_db)):
    """
        Инструкция:
        - **phone_number**: вводиться в формате 7XXXXXXXXXX (X - цифра от 0 до 9)
        - **code**: заполняется автоматически
        - **tags**: список доступных сотовых операторов 'beeline', 'mts', 'megafon', 'tele2'
        - **time_zone**: укажите свой город'
    """
    try:
        create_user(schemas, db)
        response.status_code = status.HTTP_201_CREATED
        return 'Клиент добавлен'
    except:
        raise HTTPException(status_code=400, detail='Клиент с таким номером уже есть')


@user_router.put('/user', summary="Update user information")
async def put_user(id_user: int, schemas: UserSchemas, response: Response, db: session = Depends(connect_db)):
    """
            Инструкция:
            - **phone_number**: вводиться в формате 7XXXXXXXXXX (X - цифра от 0 до 9)
            - **code**: заполняется автоматически
            - **tags**: список доступных сотовых операторов 'beeline', 'mts', 'megafon', 'tele2'
            - **time_zone**: укажите свой город'
    """

    _user = update_user(id_user, schemas, db)
    response.status_code = status.HTTP_200_OK
    return f'Клиент {_user.id} обновлён!'


@user_router.delete('/user', summary="Delete user information")
async def delete_user(id_user: int, response: Response, db: session = Depends(connect_db)):
    """
            Инструкция:
            - **id**: По указанному id будет найден и удалён клиент
    """
    remove_book(id_user, db)
    response.status_code = status.HTTP_200_OK
    return 'Клиент удалён'
