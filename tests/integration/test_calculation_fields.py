
import pytest
from uuid import uuid4
from pydantic import ValidationError

from app.models.calculation import Calculation
from app.schemas.calculation import CalculationCreate, CalculationRead


def test_create_with_a_b():
    data = CalculationCreate(
        user_id=uuid4(), type="Add", a=10, b=5
    )
    assert data.a == 10
    assert data.b == 5
    assert data.inputs == [10, 5]
    assert data.type.value == "addition"


def test_invalid_calculation_type():
    with pytest.raises(ValidationError):
        CalculationCreate(
            user_id=uuid4(), type="Unknown", a=10, b=5
        )


def test_missing_operand():
    with pytest.raises(ValidationError):
        CalculationCreate(
            user_id=uuid4(), type="Add", a=10
        )


def test_division_by_zero():
    with pytest.raises(ValidationError):
        CalculationCreate(
            user_id=uuid4(), type="Divide", a=10, b=0
        )


def test_factory_populates_a_b():
    calc = Calculation.create(
        "addition", uuid4(), [10, 5]
    )
    assert calc.a == 10
    assert calc.b == 5
    assert calc.get_result() == 15


def test_calculation_read():
    data = CalculationRead(
        id=uuid4(),
        a=10,
        b=5,
        type="addition",
        result=15
    )
    assert data.result == 15
    assert data.a == 10
    assert data.b == 5
