from fastapi import FastAPI, APIRouter
from .routers import test, user, auth, cultivo
from fastapi.responses import RedirectResponse
from .database import create_database,Base,engine
from contextlib import asynccontextmanager

router = APIRouter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    


app = FastAPI(lifespan=lifespan)    
@router.get("/")
async def root():
    return RedirectResponse("/docs")
app.include_router(router)
app.include_router(auth.router)
app.include_router(test.router)
app.include_router(user.router)
app.include_router(cultivo.router)
