from datetime import time, datetime, date, timedelta
from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from core.database import session, connect_db
from newsletter.newsletter import create_task
from newsletter.crud import create_newsletter_db, get_all_newsletter, get_one_newsletter, remove_newsletter

newsletter_router = APIRouter()


@newsletter_router.get('/all_newsletter', summary="all_newsletter")
def all_newsletter(db: session = Depends(connect_db)):
    """
            Инструкция:
            - После выполнения получите информацию о созданных рассылках
    """
    return get_all_newsletter(db)


@newsletter_router.get('/get_info_newsletter', summary="get_info_newsletter")
def get_newsletter(id_news: int, db: session = Depends(connect_db)):
    """
            Инструкция:

            - **ID** найдёт информацию по ID рассылки
    """
    return get_one_newsletter(id_news, db)


@newsletter_router.get('/create_newsletter', summary="create_newsletter")
def create_newsletter(id_news: int, text: str, date_start: date, time_start: time, date_stop: date,
                      time_stop: time, tag: str,
                      code: str = Query(max_length=3),
                      db: session = Depends(connect_db)):
    """
            Инструкция:

            - **ID**: Присвоить нужно самостоятельно (в дальнейшем можно переделать)
            - **date_start**/**date_stop**: Для удобства эти параметры вводятся отдельно
            - **date** Формат ввода 2022-12-31
            - **time** Формат ввода 23:59:59
            - **phone_number**: вводиться в формате 7XXXXXXXXXX (X - цифра от 0 до 9)
            - **code**: заполняется автоматически
            - **tags**: список доступных сотовых операторов 'beeline', 'mts', 'megafon', 'tele2'
            - **time_zone**: укажите свой город'
    """
    _date_start = datetime(date_start.year, date_start.month, date_start.day, time_start.hour, time_start.minute,
                           time_start.second)

    _date_stop = datetime(date_stop.year, date_stop.month, date_stop.day, time_stop.hour, time_stop.minute,
                          time_stop.second)

    if _date_start <= datetime.now() <= _date_stop:
        timer_start = timedelta(seconds=1)

        try:
            create_newsletter_db(id_news, _date_start, _date_stop, text, tag, code, db)
            create_task(id_news, timer_start, text, tag, code, db)
            return {'response 200': 'Рассылка отправлена'}
        except:
            return {'response 400': 'Клиент не найден или ID рассылки уже существует'}
    if _date_stop <= datetime.now() <= _date_start:
        return {'response 400': 'Вы ввели недопустимый интервал времени'}
    else:
        try:
            delta_seconds = _date_start - datetime.now()
            create_newsletter_db(id_news, _date_start, _date_stop, text, tag, code, db)
            create_task(id_news, delta_seconds, text, tag, code, db)
            return {'response 200': f'Рассылка будет запущена {_date_start}'}
        except:
            return {'response 400': 'ID рассылки уже существует'}


@newsletter_router.put('/put_newsletter', summary="put_newsletter")
def put_newsletter(response: Response, id_news: int, text: str, date_start: date, time_start: time, date_stop: date,
                   time_stop: time, tag: str,
                   code: str = Query(max_length=3),
                   db: session = Depends(connect_db)):
    """
            Инструкция:

            - **ID**: Находит по ID рассылки удаляет данные из рассылки из БД.
            Если рассылка не была запущена, то она будет отменена.
            - После этого будет создана новая рассылка взамен старой
            - **date_start**/**date_stop**: Для удобства эти параметры вводятся отдельно
            - **date** Формат ввода 2022-12-31
            - **time** Формат ввода 23:59:59
            - **phone_number**: вводиться в формате 7XXXXXXXXXX (X - цифра от 0 до 9)
            - **code**: заполняется автоматически
            - **tags**: список доступных сотовых операторов 'beeline', 'mts', 'megafon', 'tele2'
            - **time_zone**: укажите свой город'
    """
    try:
        remove_newsletter(id_news, db)
        create_newsletter(id_news, text, date_start, time_start, date_stop, time_stop, tag, code, db)
        response.status_code = status.HTTP_201_CREATED
    except:
        return {'response 400': 'Какая-то ошибка'}


@newsletter_router.delete('/all_newsletter', summary="delete_all_newsletter")
def all_newsletter(id_news: int, db: session = Depends(connect_db)):
    """
            Инструкция:

            - **ID**: Находит по ID рассылки удаляет данные из рассылки из БД.
            Если рассылка не была запущена, то она будет отменена
    """
    try:
        remove_newsletter(id_news, db)
        return {'response 200': 'ok'}
    except:
        return {'response 400': 'Какая-то ошибка'}
