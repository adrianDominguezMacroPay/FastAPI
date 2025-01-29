from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.responses import JSONResponse



class Movie(BaseModel):
    id:  Optional[int] = None
    title: str = Field(default="titulo de la pelicula", min_length=2,max_length=50)
    overview: str =Field(default="descripcion de la pelicula", min_length=3,max_length=60)
    year: int = Field(default=2021, ge=1900, le=2070)
    rating: float = Field(default=5.0, ge=0.0, le=10.0)
    category: str = Field(default="accion", min_length=2,max_length=50)


movies = [{
                "id": 1,
                "title": "Inception",
                "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                "year": 2010,
                "rating": 8.8,
                "category": "Sci-Fi"
            },
            {
                "id": 2,
                "title": "The Shawshank Redemption",
                "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                "year": 1994,
                "rating": 9.3,
                "category": "Drama"
            },
            {
                "id": 3,
                "title": "The Godfather",
                "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                "year": 1972,
                "rating": 9.2,
                "category": "Crime"
            },
            {
                "id": 4,
                "title": "The Dark Knight",
                "overview": "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.",
                "year": 2008,
                "rating": 9.0,
                "category": "Action"
            },
            {
                "id": 5,
                "title": "Pulp Fiction",
                "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
                "year": 1994,
                "rating": 8.9,
                "category": "Crime"
            }]

app = FastAPI( 
    title="FastAPI example",
    description="This is a simple example of FastAPI",
    version="0.1"
)
 
@app.get("/",tags=["inicio"])
def read_root():
    return HTMLResponse(content="<h1>Hello, world!</h1>", status_code=200)

@app.get("/movies",tags=["Movies"])
def get_movies():
    return JSONResponse(content=movies)

@app.get("/movies/{movie_id}",tags=["Movies"])
def get_movie(movie_id: int = Path(ge=1,le=50)):
    for movie in movies:
        if movie["id"] == movie_id:
            return JSONResponse(content=movie, status_code=200)
    return JSONResponse(content={"error": "Movie not found"}, status_code=404)

#para poner los query params

@app.get("/movies/", tags=["Movies"])
def get_movies(category: str = Query(default="accion", min_length=2,max_length=50)):
        return JSONResponse(content=[movie for movie in movies if movie["category"] == category], status_code=200)



@app.post("/movies",tags=["Movies"])
def create_movie(movie: Movie):
    movies.append(movie.model_dump())
    return JSONResponse(content={'message' : 'se ha cargado una nueva pelicula', 'movie' : movie.model_dump()}, status_code=201)


@app.put("/movies/{id}",tags=["Movies"])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(content={"message": "Movie updated", "movie": item}, status_code=200)
    return JSONResponse(content={"error": "Movie not found"}, status_code=404)


@app.delete("/movies/{movie_id}",tags=["Movies"])
def delete_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            movietoDelete = movie
            movies.remove(movie)
            return JSONResponse(content={"message": "Movie deleted", "movie": movietoDelete}, status_code=200)
    return JSONResponse(content={"error": "Movie not found"}, status_code=404)
