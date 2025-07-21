from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routers import aluno_router, plano_router, matricula_router

app = FastAPI()

app.include_router(aluno_router.router)
app.include_router(plano_router.router)
app.include_router(matricula_router.router)

register_tortoise(
    app,
    db_url='mysql://root:123%40GUIZINHObom@localhost:3306/wellnest_db',
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True
)