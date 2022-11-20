from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from preparing_parsed_data import *

app = FastAPI()
app.mount("/static", StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="templates")

decades, books_dates, books_by_date, books_titles = get_decades()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("centuries.html", {'request': request, 'centuries': [18, 19, 20, "Без даты"]})


@app.get("/decades", response_class=HTMLResponse)
async def decades_route(request: Request, century: str):
    if century == "Без даты":
        return templates.TemplateResponse("writings.html", {'request': request, "books": books_by_date[None], "titles": books_titles, "date": "Без даты"})
    else:
        return templates.TemplateResponse("decades.html", {'request': request, "decades": decades[int(century)]})


@app.get("/years", response_class=HTMLResponse)
def years_route(request: Request, decade: str):
    splited = decade.split("-")
    years_list = list(range(int(splited[0]), int(splited[1]) + 1))
    years = []
    for i in years_list:
        if i in books_dates:
            years.append(i)
    return templates.TemplateResponse("years.html", {'request': request, "years": years})


@app.get("/books", response_class=HTMLResponse)
def books(request: Request, book_date: str):
    print(book_date)
    if book_date is None:
        raise HTTPException(status_code=400, detail="Date is None")
    elif book_date == "null":
        book_date = None
    else:
        try:
            book_date = int(book_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Something wrong")

    if book_date not in books_by_date:
        raise HTTPException(status_code=400, detail="Something wrong")

    return templates.TemplateResponse("writings.html", {'request': request, "books": books_by_date[book_date], "titles": books_titles, "date": book_date})

