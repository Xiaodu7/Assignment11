
import os
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.user import User
from app.models.calculation import Calculation
from app.schemas.calculation import CalculationRead


@pytest.fixture(scope="module")
def db_engine():
    url = os.environ.get("TEST_DATABASE_URL")

    if not url:
        pytest.fail("TEST_DATABASE_URL is required")

    if make_url(url).database != "assignment11_test":
        pytest.fail("Use the dedicated assignment11_test database")

    engine = create_engine(url)
    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.mark.parametrize(
    "calc_type, a, b, expected",
    [
        ("addition", 10, 5, 15),
        ("subtraction", 10, 5, 5),
        ("multiplication", 10, 5, 50),
        ("division", 10, 5, 2),
    ],
)
def test_calculation_database(
    db_engine, calc_type, a, b, expected
):
    Session = sessionmaker(bind=db_engine)

    with Session() as session:
        unique_id = uuid4().hex

        user = User(
            username=f"user_{unique_id[:12]}",
            email=f"{unique_id}@example.com",
        )

        session.add(user)
        session.flush()

        calculation = Calculation.create(
            calc_type, user.id, [a, b]
        )
        calculation.result = calculation.get_result()

        session.add(calculation)
        session.commit()

        calculation_id = calculation.id

    # Read the record using a new database session
    with Session() as session:
        saved = session.get(Calculation, calculation_id)

        assert saved is not None
        assert saved.a == a
        assert saved.b == b
        assert saved.type == calc_type
        assert saved.result == expected
        assert saved.get_result() == expected

        response = CalculationRead.model_validate(saved)
        assert response.result == expected
