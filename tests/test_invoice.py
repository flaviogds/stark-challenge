import datetime
from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.core.router import api_router
from src.infra.invoice_repository import InvoiceRepository
from src.infra.stark_bank import StarkBank
from src.schemas.invoice import Invoice

#pylint: disable=W621


def create_app():
    _app = FastAPI()
    _app.include_router(api_router)
    return _app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def mock_invoice_repository():
    return MagicMock(spec=InvoiceRepository)


@pytest.fixture
def mock_starkbank():
    return MagicMock(spec=StarkBank)


@pytest.fixture
def client(app):
    return TestClient(app)


def test_create_invoice_valid_payload(client, mock_invoice_repository, mock_starkbank):
    payload = {"amount": 100, "tax_id": "123456789", "name": "John Doe"}

    with patch("src.core.invoice.InvoiceRepository", return_value=mock_invoice_repository):
        with patch("src.core.invoice.StarkBank", return_value=mock_starkbank):
            mock_starkbank.create_invoice.return_value = Invoice(
                id="invoice-1", amount=100, tax_id="123456789", name="John Doe", status="created"
            )
            mock_invoice_repository.create.return_value = {
                "id": "invoice-1",
                "amount": 100,
                "tax_id": "123456789",
                "name": "John Doe",
                "status": "created",
            }

            response = client.post("/api/v1/invoice", json=payload)

            mock_starkbank.create_invoice.assert_called_once_with(
                {
                    "id": None,
                    "amount": 100,
                    "tax_id": "123456789",
                    "name": "John Doe",
                    "status": None,
                    "descriptions": None,
                    "due": None,
                    "fine": None,
                    "interest": None,
                    "expiration": None,
                    "discounts": None,
                    "tags": None,
                    "rules": None,
                    "updated": None,
                }
            )
            mock_invoice_repository.create.assert_called_once_with(
                {
                    "id": "invoice-1",
                    "amount": 100,
                    "name": "John Doe",
                    "tax_id": "123456789",
                    "status": "created",
                    "descriptions": None,
                    "due": None,
                    "fine": None,
                    "interest": None,
                    "expiration": None,
                    "discounts": None,
                    "tags": None,
                    "rules": None,
                    "updated": None,
                }
            )
            assert response.status_code == HTTPStatus.CREATED
            assert response.json() == {
                "id": "invoice-1",
                "amount": 100,
                "tax_id": "123456789",
                "name": "John Doe",
                "status": "created",
            }


def test_create_invoice_invalid_payload(client, mock_invoice_repository, mock_starkbank):
    payload = {"amount": 0, "tax_id": "123456789", "name": ""}

    with patch("src.core.invoice.InvoiceRepository", return_value=mock_invoice_repository):
        with patch("src.core.invoice.StarkBank", return_value=mock_starkbank):
            mock_invoice_repository.create.assert_not_called()
            mock_starkbank.create_invoice.assert_not_called()

            with pytest.raises(ValueError):
                response = client.post("/api/v1/invoice", json=payload)
                assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
                raise ValueError("Invalid payload")


def test_callback_invoice_subscription_invoice(client, mock_invoice_repository, mock_starkbank):
    payload = {
        "event": {
            "subscription": "invoice",
            "log": {
                "type": "credited",
                "invoice": {"id": "invoice-1", "amount": 100, "name": "John Doe", "updated": "2022-01-01T00:00:00Z"},
            },
        }
    }
    with patch("src.core.invoice.InvoiceRepository", return_value=mock_invoice_repository):
        with patch("src.core.invoice.StarkBank", return_value=mock_starkbank):
            mock_invoice_repository.get.return_value = {
                "id": "invoice-1",
                "amount": 100,
                "name": "John Doe",
                "status": "created",
            }
            mock_starkbank.transfer_invoice.return_value = MagicMock(id="transfer-1")
            mock_invoice_repository.update.return_value = {
                "id": "invoice-1",
                "amount": 100,
                "name": "John Doe",
                "status": "paid",
                "transfer_id": "transfer-1",
                "updated": "2022-01-01T00:00:00Z",
            }
            response = client.post("/api/v1/invoice/callback", json=payload)
            assert response.status_code == HTTPStatus.OK
            assert response.json() == {
                "id": "invoice-1",
                "amount": 100,
                "name": "John Doe",
                "status": "paid",
                "transfer_id": "transfer-1",
                "updated": "2022-01-01T00:00:00Z",
            }
            mock_invoice_repository.get.assert_called_once_with("invoice-1")
            mock_starkbank.transfer_invoice.assert_called_once_with(
                {
                    "id": "invoice-1",
                    "amount": 100,
                    "name": "John Doe",
                    "tax_id": None,
                    "status": None,
                    "descriptions": None,
                    "due": None,
                    "fine": None,
                    "interest": None,
                    "expiration": None,
                    "discounts": None,
                    "tags": None,
                    "rules": None,
                    "updated": datetime.datetime(2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
                }
            )
            mock_invoice_repository.update.assert_called_once_with(
                {
                    "id": "invoice-1",
                    "amount": 100,
                    "name": "John Doe",
                    "status": "paid",
                    "transfer_id": "transfer-1",
                    "updated": datetime.datetime(2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
                }
            )


def test_callback_invoice_subscription_invoice_canceled(client, mock_invoice_repository, mock_starkbank):
    payload = {
        "event": {
            "subscription": "invoice",
            "log": {
                "type": "canceled",
                "invoice": {"id": "invoice-1", "amount": 100, "name": "John Doe", "updated": "2022-01-01T00:00:00Z"},
            },
        }
    }
    with patch("src.core.invoice.InvoiceRepository", return_value=mock_invoice_repository):
        with patch("src.core.invoice.StarkBank", return_value=mock_starkbank):
            mock_invoice_repository.get.return_value = {
                "id": "invoice-1",
                "amount": 100,
                "name": "John Doe",
                "status": "created",
            }
            mock_invoice_repository.update.return_value = {
                "id": "invoice-1",
                "amount": 100,
                "name": "John Doe",
                "status": "paid",
                "transfer_id": "transfer-1",
                "updated": "2022-01-01T00:00:00Z",
            }
            response = client.post("/api/v1/invoice/callback", json=payload)
            assert response.status_code == HTTPStatus.OK
            assert response.json() == {
                "id": "invoice-1",
                "amount": 100,
                "name": "John Doe",
                "status": "paid",
                "transfer_id": "transfer-1",
                "updated": "2022-01-01T00:00:00Z",
            }
            mock_invoice_repository.get.assert_called_once_with("invoice-1")
            mock_starkbank.transfer_invoice.assert_not_called()
            mock_invoice_repository.update.assert_called_once_with(
                {
                    "id": "invoice-1",
                    "amount": 100,
                    "name": "John Doe",
                    "status": "canceled",
                    "updated": datetime.datetime(2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
                }
            )


def test_callback_invoice_subscription_not_invoice(client, mock_invoice_repository, mock_starkbank):
    payload = {
        "event": {
            "subscription": "other",
            "log": {
                "type": "credited",
                "invoice": {"id": "invoice-1", "amount": 100.0, "name": "John Doe", "updated": "2022-01-01T00:00:00Z"},
            },
        }
    }
    with patch("src.core.invoice.InvoiceRepository", return_value=mock_invoice_repository):
        with patch("src.core.invoice.StarkBank", return_value=mock_starkbank):
            response = client.post("/api/v1/invoice/callback", json=payload)
            assert response.status_code == HTTPStatus.OK
            assert response.json() is None
            mock_invoice_repository.get.assert_not_called()
            mock_starkbank.transfer_invoice.assert_not_called()
            mock_invoice_repository.update.assert_not_called()
