import starkbank


class StarkBank: #pragma: no cover
    """
    A class representing the StarkBank API integration for invoice creation and transfer.

    Args:
        config (Config): The configuration object containing project ID, private key, and environment.

    Attributes:
        _user (starkbank.Project): The StarkBank project object.
        _transfer_account (str): The transfer account associated with the StarkBank project.

    """

    def __init__(self, config):
        self._user = starkbank.Project(
            id=config.project_id, private_key=config.private_key, environment=config.environment
        )
        self._transfer_account = config.transfer_account

    def create_invoice(self, invoice: dict):
        """
        Create a new invoice using the StarkBank API.

        Args:
            invoice (dict): A dictionary containing the invoice details.

        Returns:
            starkbank.Invoice: The created invoice object.

        """
        new_invoice = starkbank.invoice.create([starkbank.Invoice(**invoice)], self._user)
        if new_invoice:
            return new_invoice[0]
        return None

    def transfer_invoice(self, invoice: dict):
        """
        Transfer an invoice using the StarkBank API.

        Args:
            invoice (dict): A dictionary containing the invoice details.

        Returns:
            starkbank.Transfer: The created transfer object.

        """
        transfer = starkbank.transfer.create(
            [
                starkbank.Transfer(
                    amount=invoice["amount"],
                    tags=[f"invoice:{invoice['id']}", invoice["name"]],
                    **self._transfer_account,
                )
            ],
            self._user,
        )
        return transfer[0]
