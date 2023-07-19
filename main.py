from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime
import data

app = FastAPI()
app.title = 'Byhako API'
app.version = '3.4.1'

movies = data.movies

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15, default='Name')
    overview: str = Field(min_length=15, max_length=50, default='Your description')
    year: int = Field(min_length=4, max_length=4, default=datetime.date.today().year, le=datetime.date.today().year)
    rating: float = Field(ge=1, le=10, default=0)
    category: str = Field(min_length=4, max_length=15, default='Action')


@app.get('/', tags=['Home'])
def message():
    return HTMLResponse("<h1>Hola Ruben</h1>")

@app.get(
        '/movies',
        tags=['Movies'],
        response_model=List[Movie],
        status_code=200
    )
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['Movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=100)) -> Movie:
    movie = list(filter(lambda x: x['id'] == id, movies))
    code = 200 if len(movie) != 0 else 404
    return JSONResponse(status_code=code, content=movie)

@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    movie = list(filter(lambda x: x['category'] == category, movies))
    return JSONResponse(content=movie)

@app.post('/movie', tags=['Movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Creada"})

@app.put('/movie/{id}', tags=['Movies'], status_code=200)
def update_movie(id: int, movie: Movie):
    movieSelected = list(filter(lambda x: x['id'] == id, movies))[0]
    movieSelected['title'] = movie.title
    movieSelected['overview'] = movie.overview
    movieSelected['year'] = movie.year
    movieSelected['category'] = movie.category
    movieSelected['rating'] = movie.rating

    movies[id-1] = movieSelected
    return JSONResponse(status_code=200, content={"message": "Actualizada"})

@app.delete('/movie/{id}', tags=['Movies'], status_code=200)
def delete_movie(id: int):
    movies.pop(id-1)
    return JSONResponse(status_code=200, content={"message": "Borrada"})
