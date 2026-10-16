from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.dependencies import install_error_handlers
from app.domain.errors import DomainValidationError


def test_domain_error_uses_uniform_shape():
    app = FastAPI()
    install_error_handlers(app)

    @app.get("/broken")
    def broken():
        raise DomainValidationError("invalid_input", "Datos inválidos", {"amount": ["Requerido"]})

    response = TestClient(app).get("/broken")

    assert response.status_code == 422
    assert response.json() == {
        "code": "invalid_input",
        "message": "Datos inválidos",
        "field_errors": {"amount": ["Requerido"]},
    }


def test_request_validation_uses_uniform_shape():
    app = FastAPI()
    install_error_handlers(app)

    @app.get("/number")
    def number(value: int):
        return {"value": value}

    response = TestClient(app).get("/number", params={"value": "no-number"})

    assert response.status_code == 422
    assert response.json()["code"] == "validation_error"
    assert "value" in response.json()["field_errors"]
