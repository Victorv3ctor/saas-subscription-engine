from pydantic import BaseModel, ConfigDict
from datetime import datetime

class InvoiceResponseModel(BaseModel):
    model_config=ConfigDict(from_attributes=True)


    invoice_id: int
    status: str
    amount: int
    period_start: datetime
    period_end: datetime

class PayInvoiceResponseModel(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    invoice_id: int
    status: str



