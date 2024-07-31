from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from src.config import Config
from src.infra.invoice_repository import InvoiceRepository
from src.infra.stark_bank import StarkBank
from src.schemas.invoice import Invoice, RequestPayload

invoice = APIRouter()

_database = Annotated[InvoiceRepository, Depends(lambda: InvoiceRepository(Config()))]
_starkbank = Annotated[StarkBank, Depends(lambda: StarkBank(Config()))]


@invoice.post("/invoice", status_code=HTTPStatus.CREATED)
async def create_invoice(payload: Invoice, database: _database, starkbank: _starkbank):
    """
    Create an invoice using the provided payload.

    Args:
        payload (Invoice): The payload containing the invoice details.
        database (_database): The database object used to store the created invoice.
        starkbank (_starkbank): The Starkbank object used to create the invoice.

    Returns:
        dict: The created invoice details if successful, None otherwise.

    Raises:
        ValueError: If the payload is invalid.
    """
    if all([payload.amount > 0, payload.tax_id, payload.name]):
        new_invoice = starkbank.create_invoice(payload.model_dump())
        if new_invoice:
            return database.create(new_invoice.__dict__)
        return None
    raise ValueError("Invalid payload")


@invoice.post("/invoice/callback", status_code=HTTPStatus.OK)
async def callback_invoice(payload: RequestPayload, database: _database, starkbank: _starkbank):
    """
    Callback function for invoice events.

    Args:
        payload (RequestPayload): The payload containing the event data.
        database (_database): The database object for accessing and updating invoice data.
        starkbank (_starkbank): The Starkbank object for performing invoice-related operations.

    Returns:
        dict: The updated invoice data in the database, or None if no update is needed.
    """
    if payload.event.subscription == "invoice":
        _invoice = database.get(payload.event.log.invoice.id)
        if payload.event.log.type == "credited" and _invoice["status"] == "created":
            transfer = starkbank.transfer_invoice(payload.event.log.invoice.model_dump())
            _invoice["status"] = "paid"
            _invoice["transfer_id"] = transfer.id
        if payload.event.log.type == "canceled":
            _invoice["status"] = "canceled"
        _invoice["updated"] = payload.event.log.invoice.updated
        return database.update(_invoice)
    return None
