class InvoiceNotFound(Exception):
    detail='invoice not  found'


class WrongInvoiceStatus(Exception):
    detail='wrong invoice status'