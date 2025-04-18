import pytest
from httpx import AsyncClient, ASGITransport

from app import app

@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post("/setup_database")
        await ac.post("/books", json={"title": "Book 1", "author": "Author 1"})
        await ac.post("/books", json={"title": "Book 2", "author": "Author 2"})
        response = await ac.get("/books")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
