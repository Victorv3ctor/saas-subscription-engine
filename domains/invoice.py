from datetime import datetime, timedelta
from exceptions.invoice import WrongInvoiceStatus

class Invoice:
    def __init__(
            self,
            sub_id,
            status, #pending/paid/expired/
            amount,
            period_start,
            period_end,
            invoice_id: None = None
    ):
        self.sub_id = sub_id
        self.status = status
        self.amount = amount
        self.period_start = period_start
        self.period_end = period_end
        self.invoice_id = invoice_id


    @classmethod
    def create(cls, subscription_id
               ):
        return cls(
            sub_id=subscription_id,
            status='pending',
            amount=45,
            period_start=datetime.now().date(),
            period_end=datetime.now().date() + timedelta(days=30)
        )

#The option to cancel invoice is only for pending status
    #we cant cancel paid or expired invoice
    def cancel(self):
        if self.status == 'pending':
            self.status = 'canceled'
        return

    def pay(self):
        if self.status !='pending':
            raise WrongInvoiceStatus()
        self.status = 'paid'









