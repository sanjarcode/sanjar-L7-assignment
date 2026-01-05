from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import models, schemas, crud
from database import engine, get_db, Base

app = FastAPI(title="Movie Explorer API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for assignment purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/movies/", response_model=schemas.Movie)
async def create_movie(movie: schemas.MovieCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_movie(db=db, movie=movie)

@app.get("/movies/", response_model=List[schemas.Movie])
async def read_movies(
    skip: int = 0,
    limit: int = 100,
    genre: Optional[str] = None,
    director: Optional[str] = None,
    actor: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_movies(db, skip=skip, limit=limit, genre=genre, director=director, actor=actor, search=search)

@app.get("/movies/{movie_id}", response_model=schemas.Movie)
async def read_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    db_movie = await crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@app.get("/actors/{actor_id}", response_model=schemas.Actor)
async def read_actor(actor_id: int, db: AsyncSession = Depends(get_db)):
    db_actor = await crud.get_actor(db, actor_id=actor_id)
    if db_actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return db_actor

@app.get("/directors/{director_id}", response_model=schemas.Director)
async def read_director(director_id: int, db: AsyncSession = Depends(get_db)):
    db_director = await crud.get_director(db, director_id=director_id)
    if db_director is None:
        raise HTTPException(status_code=404, detail="Director not found")
    return db_director

@app.get("/genres/", response_model=List[schemas.Genre])
async def read_genres(db: AsyncSession = Depends(get_db)):
    return await crud.get_genres(db)

@app.get("/actors/", response_model=List[schemas.ActorMinimal])
async def read_actors(db: AsyncSession = Depends(get_db)):
    return await crud.get_actors(db)

@app.get("/directors/", response_model=List[schemas.DirectorMinimal])
async def read_directors(db: AsyncSession = Depends(get_db)):
    return await crud.get_directors(db)

# Simple health check
@app.get("/")
def read_root():
    return {"message": "Welcome to Movie Explorer API"}
