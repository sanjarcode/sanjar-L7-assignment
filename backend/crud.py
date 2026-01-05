from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
import models, schemas
from typing import List, Optional

async def get_or_create_director(db: AsyncSession, name: str) -> models.Director:
    result = await db.execute(select(models.Director).where(models.Director.name == name))
    director = result.scalars().first()
    if not director:
        director = models.Director(name=name)
        db.add(director)
        await db.commit()
        await db.refresh(director)
    return director

async def get_or_create_genre(db: AsyncSession, name: str) -> models.Genre:
    result = await db.execute(select(models.Genre).where(models.Genre.name == name))
    genre = result.scalars().first()
    if not genre:
        genre = models.Genre(name=name)
        db.add(genre)
        await db.commit()
        await db.refresh(genre)
    return genre

async def get_or_create_actor(db: AsyncSession, name: str) -> models.Actor:
    result = await db.execute(select(models.Actor).where(models.Actor.name == name))
    actor = result.scalars().first()
    if not actor:
        actor = models.Actor(name=name)
        db.add(actor)
        await db.commit()
        await db.refresh(actor)
    return actor

async def create_movie(db: AsyncSession, movie: schemas.MovieCreate):
    director = await get_or_create_director(db, movie.director_name)

    genres = []
    for g_name in movie.genre_names:
        genres.append(await get_or_create_genre(db, g_name))

    actors = []
    for a_name in movie.actor_names:
        actors.append(await get_or_create_actor(db, a_name))

    db_movie = models.Movie(
        title=movie.title,
        release_year=movie.release_year,
        director=director,
        genres=genres,
        actors=actors
    )
    db.add(db_movie)
    await db.commit()
    await db.refresh(db_movie)
    # Reload with relationships for Pydantic serialization
    return await get_movie(db, db_movie.id)

async def get_movies(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    genre: Optional[str] = None,
    director: Optional[str] = None,
    actor: Optional[str] = None,
    search: Optional[str] = None,
    release_year: Optional[int] = None
):
    query = select(models.Movie).options(
        selectinload(models.Movie.director),
        selectinload(models.Movie.genres),
        selectinload(models.Movie.actors)
    )

    if genre:
        query = query.join(models.Movie.genres).where(models.Genre.name.ilike(f"%{genre}%"))
    if director:
        query = query.join(models.Movie.director).where(models.Director.name.ilike(f"%{director}%"))
    if actor:
        query = query.join(models.Movie.actors).where(models.Actor.name.ilike(f"%{actor}%"))
    if search:
        query = query.where(models.Movie.title.ilike(f"%{search}%"))
    if release_year:
        query = query.where(models.Movie.release_year == release_year)

    # Deduplicate if joins cause duplicates (though selectinload handles joins differently for loading, explicit joins for filtering might need distinct)
    # However, standard join on many-to-many might duplicate rows. distinct() helps.
    # query = query.distinct() # Basic distinct

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_movie(db: AsyncSession, movie_id: int):
    query = select(models.Movie).options(
        selectinload(models.Movie.director),
        selectinload(models.Movie.genres),
        selectinload(models.Movie.actors)
    ).where(models.Movie.id == movie_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_actor(db: AsyncSession, actor_id: int):
    query = select(models.Actor).options(
        selectinload(models.Actor.movies).selectinload(models.Movie.genres)
        # Deep loading might be needed depending on what we show
    ).where(models.Actor.id == actor_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_director(db: AsyncSession, director_id: int):
    query = select(models.Director).options(
        selectinload(models.Director.movies)
    ).where(models.Director.id == director_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_genres(db: AsyncSession):
    result = await db.execute(select(models.Genre).order_by(models.Genre.name))
    return result.scalars().all()

async def get_actors(db: AsyncSession, movie: Optional[str] = None, genre: Optional[str] = None):
    query = select(models.Actor).order_by(models.Actor.name)
    if movie:
        query = query.join(models.Actor.movies).where(models.Movie.title.ilike(f"%{movie}%"))
    if genre:
        query = query.join(models.Actor.movies).join(models.Movie.genres).where(models.Genre.name.ilike(f"%{genre}%"))

    if movie or genre:
        query = query.distinct()

    result = await db.execute(query)
    return result.scalars().all()

async def get_directors(db: AsyncSession):
    result = await db.execute(select(models.Director).order_by(models.Director.name))
    return result.scalars().all()
