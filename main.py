from fastapi import FastAPI
import uvicorn
from config.settings import settings
from tortoise.contrib.fastapi import register_tortoise
from apps.users.routers import router as user_router


app = FastAPI(docs_url="/swagger",debug=settings.DEBUG)
app.include_router(user_router)

register_tortoise(
    app,
    db_url=f"postgres://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
    generate_schemas=True,
    modules={"models":['apps.users.models']},
    add_exception_handlers = True
)


if __name__  == "__main__":
    uvicorn.run("main:app",reload=settings.RELOAD,host=settings.HOST,port=settings.PORT)
