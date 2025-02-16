from fastapi import FastAPI, APIRouter, BackgroundTasks
from .routers import test, user, auth, cultivo, localidad, historico, previcion
from fastapi.responses import RedirectResponse
from .database import get_db,Base,engine
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from .interceptor.predict import predict

router = APIRouter()
# templates = Jinja2Templates(directory="/home/rafa/Projects/Python/api-clima/frontend/dist/front/browser/")

origins = [
    "http://localhost:8080",
    "http://localhost:4200",
 ]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    
def fetch_request(db):
    # with aiohttp.ClientSession() as session:
    #     with session.get("http://127.0.0.1:8000/api/start-previcion") as response:

    # print(requests.get("http://127.0.0.1:8000/api/start-previcion"))
    predict(next(db))    

    


app = FastAPI(lifespan=lifespan)    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="../frontend/dist/front/browser/"), name="static")
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_request, 'cron', hour=15, minute=7, args=(get_db(),))  # Executa às 00:00 todos os dias
scheduler.start()

# @router.get("/")
# async def root(request: Request):
    
#     return templates.TemplateResponse("index.html", {"request": request})
app.include_router(router)
app.include_router(auth.router)
app.include_router(test.router)
app.include_router(user.router)
app.include_router(cultivo.router)
app.include_router(historico.router)
app.include_router(localidad.router)
app.include_router(previcion.router)


