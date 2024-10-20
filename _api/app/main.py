from fastapi import FastAPI, APIRouter, Request
from .routers import test, user, auth, cultivo, localidad
from fastapi.responses import RedirectResponse
from .database import create_database,Base,engine
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter()
# templates = Jinja2Templates(directory="/home/rafa/Projects/Python/api-clima/frontend/dist/front/browser/")

origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
    '*'
 ]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    


app = FastAPI(lifespan=lifespan)    
# app.mount("/static", StaticFiles(directory="../frontend/dist/front/browser/"), name="static")

# @router.get("/")
# async def root(request: Request):
    
#     return templates.TemplateResponse("index.html", {"request": request})
app.include_router(router)
app.include_router(auth.router)
app.include_router(test.router)
app.include_router(user.router)
app.include_router(cultivo.router)
app.include_router(localidad.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

