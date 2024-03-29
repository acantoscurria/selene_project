from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_create_user():
    user_data = {
        "cuit": "20345678901",
        "name": "John Doe",
        "birthdate": "1985-08-15",
        "gender": "male",
        "address": {
            "street_name": "Maple Street",
            "street_number": 123,
            "floor": 2,
            "apartment": "B",
            "zip_code": 54321,
            "neighborhood": "Suburbia",
            "city": "Metropolis",
            "country": "United States",
            "additional_info": "Close to the park",
        },
    }

    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201
    user = response.json()
    print(user)
    assert user["name"] == user_data["name"]
    assert user["cuit"] == user_data["cuit"]
