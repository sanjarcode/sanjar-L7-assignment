import asyncio
from database import AsyncSessionLocal, engine, Base
import models
from sqlalchemy.future import select

async def get_or_create(session, model, **kwargs):
    result = await session.execute(select(model).filter_by(**kwargs))
    instance = result.scalars().first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    return instance

async def populate():
    async with AsyncSessionLocal() as session:
        # Create Tables (if not exist, though usually main app does this)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("Creating Mock Data...")

        # Directors
        nolan = await get_or_create(session, models.Director, name="Christopher Nolan")
        tarantino = await get_or_create(session, models.Director, name="Quentin Tarantino")
        villeneuve = await get_or_create(session, models.Director, name="Denis Villeneuve")

        # Genres
        scifi = await get_or_create(session, models.Genre, name="Sci-Fi")
        action = await get_or_create(session, models.Genre, name="Action")
        drama = await get_or_create(session, models.Genre, name="Drama")
        crime = await get_or_create(session, models.Genre, name="Crime")

        # Actors
        leo = await get_or_create(session, models.Actor, name="Leonardo DiCaprio")
        murphy = await get_or_create(session, models.Actor, name="Cillian Murphy")
        chalamet = await get_or_create(session, models.Actor, name="Timothée Chalamet")
        zendaya = await get_or_create(session, models.Actor, name="Zendaya")
        travolta = await get_or_create(session, models.Actor, name="John Travolta")
        jackson = await get_or_create(session, models.Actor, name="Samuel L. Jackson")

        # Movies
        inception = await get_or_create(session, models.Movie, title="Inception", release_year=2010)
        inception.director = nolan
        if scifi not in inception.genres: inception.genres.append(scifi)
        if action not in inception.genres: inception.genres.append(action)
        if leo not in inception.actors: inception.actors.append(leo)
        if murphy not in inception.actors: inception.actors.append(murphy)

        dune = await get_or_create(session, models.Movie, title="Dune: Part One", release_year=2021)
        dune.director = villeneuve
        if scifi not in dune.genres: dune.genres.append(scifi)
        if drama not in dune.genres: dune.genres.append(drama)
        if chalamet not in dune.actors: dune.actors.append(chalamet)
        if zendaya not in dune.actors: dune.actors.append(zendaya)

        pulp = await get_or_create(session, models.Movie, title="Pulp Fiction", release_year=1994)
        pulp.director = tarantino
        if crime not in pulp.genres: pulp.genres.append(crime)
        if drama not in pulp.genres: pulp.genres.append(drama)
        if travolta not in pulp.actors: pulp.actors.append(travolta)
        if jackson not in pulp.actors: pulp.actors.append(jackson)

        await session.commit()
        print("Mock Data Inserted!")

if __name__ == "__main__":
    asyncio.run(populate())
