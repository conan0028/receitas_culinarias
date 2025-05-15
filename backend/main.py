from fastapi import FastAPI
from backend.routers import (
    cozinheiros_router,
    degustadores_router,
    editores_router,
    livros_router,
    restaurantes_router,
    categorias_router,
    ingredientes_router,
    empregados_router,
    receitas_router,
    inclui_router,
    ingredientes_receita_router,
    restaurantes_cozinheiro_router,
    testa_router,
    possui_router
)
from backend.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(cozinheiros_router.router)
app.include_router(degustadores_router.router)
app.include_router(editores_router.router)
app.include_router(livros_router.router)
app.include_router(restaurantes_router.router)
app.include_router(categorias_router.router)
app.include_router(ingredientes_router.router)
app.include_router(empregados_router.router)
app.include_router(receitas_router.router)
app.include_router(inclui_router.router)
app.include_router(ingredientes_receita_router.router)
app.include_router(restaurantes_cozinheiro_router.router)
app.include_router(testa_router.router)
app.include_router(possui_router.router)