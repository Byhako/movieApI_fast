from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
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

@app.get('/movies', tags=['Movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=100)):
    movie = filter(lambda x: x['id'] == id, movies )
    return list(movie)

@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    movie = filter(lambda x: x['category'] == category, movies)
    return list(movie)

@app.post('/movie', tags=['Movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies

@app.put('/movie/{id}', tags=['Movies'])
def update_movie(id: int, movie: Movie):
    movieSelected = list(filter(lambda x: x['id'] == id, movies))[0]
    movieSelected['title'] = movie.title
    movieSelected['overview'] = movie.overview
    movieSelected['year'] = movie.year
    movieSelected['category'] = movie.category
    movieSelected['rating'] = movie.rating

    movies[id-1] = movieSelected
    return movies

@app.delete('/movie/{id}', tags=['Movies'])
def delete_movie(id: int):
    movies.pop(id-1)
    return movies
