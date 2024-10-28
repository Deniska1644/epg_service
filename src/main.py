from fastapi import FastAPI
import uvicorn
from auth.routers import router as auth_router
from dateapp.routers import router as date_app_router


app = FastAPI()


app.include_router(auth_router)
app.include_router(date_app_router)


if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='localhost',
        port=8000
    )
