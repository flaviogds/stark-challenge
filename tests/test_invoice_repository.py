from unittest.mock import MagicMock
import pytest
from google.cloud import firestore
from mockfirestore import MockFirestore

from src.infra.invoice_repository import InvoiceRepository

#pylint: disable=W621


class MockFirestorePlus(MockFirestore):

    def from_service_account_info(self, _):
        return MockFirestore()


@pytest.fixture
def mock_firestore():
    firestore.Client = MockFirestorePlus
    yield
    firestore.Client = firestore.Client


@pytest.fixture
def invoice_repository(mock_firestore):
    config = MagicMock()
    config.credentials = {
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id",
        "private_key": "your-private-key",
        "client_email": "your-client-email",
        "client_id": "your-client-id",
        "auth_uri": "your-auth-uri",
        "token_uri": "your-token-uri",
        "auth_provider_x509_cert_url": "your-auth-provider-x509-cert-url",
        "client_x509_cert_url": "your-client-x509-cert-url",
    }
    return InvoiceRepository(config)


def test_create_invoice(invoice_repository):
    invoice_data = {"id": "invoice-1", "amount": 100, "customer": "John Doe"}
    created_invoice = invoice_repository.create(invoice_data)
    assert created_invoice == invoice_data


def test_create_invoice_invalid_or_missing_id_key(invoice_repository):
    invoice_data = {"invalid-our-missing-id-key": "invoice-1", "amount": 100, "customer": "John Doe"}
    with pytest.raises(KeyError):
        invoice_repository.create(invoice_data)


def test_update_invoice(invoice_repository):
    invoice_data = {"id": "invoice-1", "amount": 100, "customer": "John Doe"}
    invoice_repository.create(invoice_data)

    invoice_data = {"id": "invoice-1", "amount": 200, "customer": "Jane Smith"}
    updated_invoice = invoice_repository.update(invoice_data)
    assert updated_invoice == invoice_data


def test_update_invoice_invalid_or_missing_id_key(invoice_repository):
    invoice_data = {"invalid-our-missing-id-key": "invoice-1", "amount": 100, "customer": "John Doe"}
    with pytest.raises(KeyError):
        invoice_repository.create(invoice_data)


def test_get_invoice(invoice_repository):
    invoice_id = "invoice-1"
    invoice_data = {"id": invoice_id, "amount": 100, "customer": "Jane Smith"}
    invoice_repository.db.collection("invoices").document(invoice_id).set(invoice_data)
    retrieved_invoice = invoice_repository.get(invoice_id)
    assert retrieved_invoice == invoice_data


def test_get_invoice_invalid_id(invoice_repository):
    invoice_id = "invoice-1"
    invoice_data = {"id": invoice_id, "amount": 100, "customer": "Jane Smith"}
    invoice_repository.db.collection("invoices").document("invoice_id").set(invoice_data)
    assert invoice_repository.get("invalid-invoice-id") is None
