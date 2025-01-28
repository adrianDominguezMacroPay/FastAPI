from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional



class Movie(BaseModel):
    id:  Optional[int] = None
    title: str
    overview: str
    year: int
    rating: float
    category: str


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
    return { movies }

@app.get("/movies/{movie_id}",tags=["Movies"])
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return {"error": "Movie not found"}


#para poner los query params

@app.get("/movies/", tags=["Movies"])
def get_movies(category: str):
        return category



@app.post("/movies",tags=["Movies"])
def create_movie(movie: Movie):
    print(movies.count)
    movies.append(movie)
    print(movies.count)
    return movies


@app.put("/movies/{id}",tags=["Movies"])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return item
    return {"error": "Movie not found"}


@app.delete("/movies/{movie_id}",tags=["Movies"])
def delete_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            movies.remove(movie)
            return {"message": "Movie deleted"}
    return {"error": "Movie not found"}
