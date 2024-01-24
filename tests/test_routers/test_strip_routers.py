import pytest
from fastapi.testclient import TestClient
from main import app
import httpx


client = TestClient(app)

@pytest.mark.asyncio
async def test_stripe_checkout():
    async with httpx.AsyncClient() as client:
        # Simulez une requête GET vers /stripe/checkout
        response = await client.get("http://localhost/stripe/checkout")

        # Assurez-vous que la réponse a un code d'état 404 OK
        assert response.status_code == 404