import datetime
from google.cloud import firestore


class InvoiceRepository:
    """
    A class representing a repository for managing invoices in the database.
    """

    def __init__(self, config):
        self.db = firestore.Client().from_service_account_info(config.credentials)

    def create(self, invoice):
        """
        Creates a new invoice in the database.

        Args:
            invoice (dict): The invoice data to be stored in the database.

        Returns:
            dict: The created invoice data retrieved from the database.
        """
        document = self.db.collection("invoices").document(invoice["id"])
        data_normailized = self._convert_datetime_fields(invoice)
        document.set(data_normailized)
        return document.get().to_dict()

    def update(self, invoice):
        """
        Updates an invoice in the database.

        Args:
            invoice (dict): The invoice data to be updated.

        Returns:
            dict: The updated invoice data.
        """
        document = self.db.collection("invoices").document(invoice["id"])
        data_normailized = self._convert_datetime_fields(invoice)
        document.set(data_normailized)
        return document.get().to_dict()

    def get(self, invoice_id):
        """
        Retrieves an invoice from the database based on the given invoice_id.

        Args:
            invoice_id (str): The ID of the invoice to retrieve.

        Returns:
            dict: A dictionary representing the invoice data.
        """
        doc_ref = self.db.collection("invoices").document(invoice_id)
        document = doc_ref.get()
        if document.exists:
            return document.to_dict()
        return None

    @staticmethod
    def _convert_datetime_fields(data): #pragma: no cover
        for key, value in data.items():
            if isinstance(value, datetime.datetime):
                data[key] = value.isoformat()
            elif isinstance(value, datetime.timedelta):
                data[key] = value.total_seconds()
        return data
