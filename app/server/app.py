from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import pathlib



from .routes.student import router as StudentRouter

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")


BASE_DIR = pathlib.Path(__file__).parent.parent
templates = Jinja2Templates(directory=[
    BASE_DIR / "front" / "templates",
])

app.mount("/static", StaticFiles(directory= (BASE_DIR / "front" / "static")), name="static")

"""
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
"""

#Маршрутизация выдачи главной страницы
@app.get('/', response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    response = templates.TemplateResponse("main.html", {"request": request})  # Передаем request
    return response

#Маршрутизация выдачи страницы добавления студента    
@app.get("/std_add.html", response_class=HTMLResponse)
async def std_add(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("std_add.html", {"request": request})

#Маршрутизация выдачи страницы удаления студента
@app.get("/std_del.html", response_class=HTMLResponse)
async def std_del(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("std_del.html", {"request": request})

#Маршрутизация выдачи страницы добавления пароля
@app.get("/pwd_add.html", response_class=HTMLResponse)
async def pwd_add(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("pwd_add.html", {"request": request})

#Маршрутизация выдачи страницы удаления пароля
@app.get("/pwd_del.html", response_class=HTMLResponse)
async def pwd_del(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("pwd_del.html", {"request": request})

#Маршрутизация выдачи страницы получения данных для входа
@app.get("/get_pwd_name.html", response_class=HTMLResponse)
async def get_pwd_name(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("get_pwd_name.html", {"request": request})
    