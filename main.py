import uvicorn
from fastapi import FastAPI
from core.config import ROUT, PORT
from user.api import user_router
from newsletter.api import newsletter_router
from message.api import message_router

app = FastAPI()

app.include_router(user_router, tags=["User"])
app.include_router(newsletter_router, tags=["Newsletter"])
app.include_router(message_router, tags=["Message"])

if __name__ == '__main__':
    uvicorn.run(ROUT, port=PORT, reload=True)
