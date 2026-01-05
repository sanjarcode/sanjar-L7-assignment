import json
import asyncio
import random
import os
from datetime import datetime
from database import AsyncSessionLocal, engine, Base
import models
from sqlalchemy.future import select

async def populate():
    async with AsyncSessionLocal() as session:
        # Reset Database
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        print("Database reset. Creating Mock Data from JSON...")

        # Load JSON
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(current_dir, "movies_data.json")
            with open(json_path, "r") as f:
                data = json.load(f)
                movies_list = data.get("data", [])
        except FileNotFoundError:
            print("Error: movies_data.json not found!")
            return

        # Caches to avoid DB lookups during batch processing
        genres_cache = {}
        directors_cache = {}
        actors_cache = {}

        # Helper to get/create in memory
        def get_cached_or_new(model, cache, name, profile_url=None):
            if name in cache:
                return cache[name]
            instance = model(name=name, profile_url=profile_url)
            session.add(instance)
            cache[name] = instance
            return instance

        # Pre-create Genres
        genres_names = ["Action", "Adventure", "Sci-Fi", "Drama", "Crime", "Comedy", "Thriller", "Horror", "Romance", "Fantasy", "Animation", "Mystery"]
        for g_name in genres_names:
            if g_name not in genres_cache:
                genre = models.Genre(name=g_name)
                session.add(genre)
                genres_cache[g_name] = genre

        # Pre-create Directors (Random pool since JSON lacks them)
        directors_names = [
            "Christopher Nolan", "Steven Spielberg", "Quentin Tarantino", "Martin Scorsese",
            "James Cameron", "Greta Gerwig", "Ridley Scott", "Denis Villeneuve",
            "Wes Anderson", "David Fincher", "Coen Brothers", "Spike Lee"
        ]
        for d_name in directors_names:
            get_cached_or_new(models.Director, directors_cache, d_name)

        print(f"Processing {len(movies_list)} movies...")

        for movie_data in movies_list:
            title = movie_data.get("original_title")
            release_date_str = movie_data.get("release_date")
            poster_url = movie_data.get("poster_path")

            # Parse Year
            year = 2000 # Default
            if release_date_str:
                try:
                    dt = datetime.strptime(release_date_str, "%a, %m/%d/%Y")
                    year = dt.year
                except ValueError:
                    try:
                        year = int(release_date_str[:4])
                    except:
                        pass

            movie = models.Movie(title=title, release_year=year, poster_url=poster_url)
            session.add(movie)

            # Assign Random Director
            import random # Re-import inside just in case, though logically top-level is fine
            d_name = random.choice(directors_names)
            movie.director = directors_cache[d_name]

            # Assign Random Genres (1-3)
            g_names = random.sample(genres_names, k=random.randint(1, 3))
            for g_name in g_names:
                movie.genres.append(genres_cache[g_name])

            # Assign Actors
            casts = movie_data.get("casts", [])
            for cast_member in casts[:8]:
                actor_name = cast_member.get("name")
                profile_url = cast_member.get("profile_path")
                if actor_name:
                    actor = get_cached_or_new(models.Actor, actors_cache, actor_name, profile_url=profile_url)
                    # Since we are building graph in memory, simple append works
                    # Check list to avoid duplicate actor in same movie
                    if actor not in movie.actors:
                        movie.actors.append(actor)

        print("Committing to database (this might take a moment)...")
        await session.commit()
        print(f"Successfully populated database with {len(movies_list)} movies!")

if __name__ == "__main__":
    asyncio.run(populate())
