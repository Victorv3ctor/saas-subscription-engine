from database.transaction import transaction

from exceptions.invoice import InvoiceNotFound

from repository.repository import (
    get_invoice_by_sub_id, get_invoices_list_by_user_id,update_invoice_status,
    expire_invoice
)

def cancel_invoice(conn, sub_id):
    invoice = get_invoice_by_subscription_id(conn, sub_id)
    invoice.cancel()
    expire_invoice(conn, invoice)

def mark_invoice_paid(user_id, invoice_id):
    with transaction() as conn:
        invoice = get_invoice_by_invoice_id(conn, user_id, invoice_id)
        if not invoice:
            raise InvoiceNotFound()
        invoice.pay()
        update_invoice_status(conn, invoice)
        return invoice



"""QUERY"""
def get_invoice_by_subscription_id(conn, sub_id):
    invoice = get_invoice_by_sub_id(conn, sub_id)
    if not invoice:
        raise InvoiceNotFound()
    return invoice

def get_invoices_by_user_id(user_id):
    with transaction() as conn:
        invoices = get_invoices_list_by_user_id(conn, user_id)
        if not invoices:
            raise InvoiceNotFound()
        return invoices

def get_invoice_by_invoice_id(conn, user_id, invoice_id):
    invoices = get_invoices_list_by_user_id(conn, user_id)
    return next(
        (invoice for invoice in invoices
        if invoice.invoice_id == invoice_id),
        None)








































