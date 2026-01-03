import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from database import Base, engine, get_db
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine_test = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
async def client():
    # Create tables
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    # Drop tables (optional, or rely on temp db file)
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_movie(client):
    response = await client.post(
        "/movies/",
        json={
            "title": "Inception",
            "release_year": 2010,
            "director_name": "Christopher Nolan",
            "genre_names": ["Sci-Fi", "Thriller"],
            "actor_names": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Inception"
    assert data["director"]["name"] == "Christopher Nolan"
    assert len(data["genres"]) == 2

@pytest.mark.asyncio
async def test_read_movies(client):
    response = await client.get("/movies/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Inception"
