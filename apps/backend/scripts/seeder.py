from config.settings import UserModel, RoleModel, MunicipalityModel, TechnicalSheet, SessionLocal
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_users_and_sheets():
    db = SessionLocal()

    roles = [
        RoleModel(name="Admin"),
        RoleModel(name="Citizen")
    ]
    db.add_all(roles)
    db.commit()

    municipality = MunicipalityModel(name="Municipality 1")
    db.add(municipality)
    db.commit()

    users = [
        UserModel(
            name="Admin User",
            email="admin@example.com",
            password=pwd_context.hash("adminpassword"),
            id_municipio=municipality.id,
            role_id=roles[0].id
        ),
        UserModel(
            name="Citizen User",
            email="citizen@example.com",
            password=pwd_context.hash("citizenpassword"),
            id_municipio=municipality.id,
            role_id=roles[1].id
        )
    ]
    db.add_all(users)
    db.commit()

    sheets = [
        TechnicalSheet(
            id=1,
            uuid="uuid-001",
            address="Main Street 123",
            square_meters="100",
            coordinates="POINT(19.4326 -99.1332)",
            image="image1.jpg",
            municipality_id=municipality.id,
            created_at=datetime(2023, 10, 1, 12, 0),
            updated_at=datetime(2023, 10, 1, 12, 0)
        ),
        TechnicalSheet(
            id=2,
            uuid="uuid-002",
            address="Elm Street 456",
            square_meters="150",
            coordinates="POINT(18.4861 -69.9312)",
            image="image2.jpg",
            municipality_id=municipality.id,
            created_at=datetime(2023, 10, 1, 14, 0),
            updated_at=datetime(2023, 10, 1, 14, 0)
        ),
        TechnicalSheet(
            id=3,
            uuid="uuid-003",
            address="Sunset Blvd 789",
            square_meters="200",
            coordinates="POINT(20.6597 -103.3496)",
            image="image3.jpg",
            municipality_id=municipality.id,
            created_at=datetime(2023, 10, 2, 9, 30),
            updated_at=datetime(2023, 10, 2, 9, 30)
        ),
        TechnicalSheet(
            id=4,
            uuid="uuid-004",
            address="5th Avenue 101",
            square_meters="120",
            coordinates="POINT(34.0522 -118.2437)",
            image="image4.jpg",
            municipality_id=municipality.id,
            created_at=datetime(2024, 1, 15, 8, 0),
            updated_at=datetime(2024, 1, 15, 8, 0)
        ),
        TechnicalSheet(
            id=5,
            uuid="uuid-005",
            address="Broadway 202",
            square_meters="90",
            coordinates="POINT(40.7128 -74.0060)",
            image="image5.jpg",
            municipality_id=municipality.id,
            created_at=datetime(2024, 1, 15, 10, 15),
            updated_at=datetime(2024, 1, 15, 10, 15)
        ),
        TechnicalSheet(
            id=6,
            uuid="uuid-000",
            address="Old Road 999",
            square_meters="50",
            coordinates="POINT(0 0)",
            image="old.jpg",
            municipality_id=municipality.id,
            created_at=datetime(2021, 1, 1, 0, 0),
            updated_at=datetime(2021, 1, 1, 0, 0)
        ),
    ]

    db.add_all(sheets)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_users_and_sheets()
