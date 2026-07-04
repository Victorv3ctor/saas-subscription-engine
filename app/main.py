from fastapi import FastAPI, Depends

from services.user_service import new_user
from services.invoice_service import get_invoices_by_user_id, mark_invoice_paid
from services.subscription_service import (
    set_new_subscription, subscription_and_inv_cancel, subscription_query, change_current_sub
)
from services.auth import login_in, get_current_account
from app.handlers import exception_handlers

from schemas.user import RegisterRequest, LoginRequest, RegisterResponse
from schemas.subscription import (
    CancelSubscriptionResponse, SubscriptionRequest,
    ChangeSubscriptionRequest, SubscriptionResponse)
from schemas.invoice import InvoiceResponseModel, PayInvoiceResponseModel
app = FastAPI()

exception_handlers(app)


@app.post('/register', tags=['LogIn'], response_model=RegisterResponse)
def register(
        data: RegisterRequest,
):
    return new_user(
        data.username,
        data.pwd,
        data.email
        )

@app.post('/login', tags=['LogIn'])
def login(
        data: LoginRequest,
):
    return login_in(data.username, data.pwd)

@app.post('/subscriptions/upgrade', tags=['Subscription'], response_model=SubscriptionResponse)
def start_subscription(
        data: SubscriptionRequest,
        user = Depends(get_current_account),
):
    return set_new_subscription(
        user_id=user.user_id,
        data_plan=data.plan,
        data_duration=data.duration
    )

@app.post('/subscriptions/cancel', tags=['Subscription'], response_model=CancelSubscriptionResponse)
def cancel_subscription(
        user = Depends(get_current_account),
):
    return subscription_and_inv_cancel(
        user_id=user.user_id
    )

@app.get('/subscriptions/me', tags=['Subscription'], response_model=SubscriptionResponse)
def my_subscription(
        user=Depends(get_current_account),
):
    return subscription_query(
        user_id=user.user_id
    )



@app.patch('/subscriptions/update', tags=['Subscription'], response_model=SubscriptionResponse)
def change_subscription_plan(
        data: ChangeSubscriptionRequest,
        user = Depends(get_current_account),
):
    return change_current_sub(user.user_id, data.plan, data.duration)


@app.get('/invoices/me', tags=['Invoice'], response_model=list[InvoiceResponseModel])
def show_my_invoices(
        user = Depends(get_current_account)
):
    return get_invoices_by_user_id(user_id=user.user_id)


@app.patch('/invoices/invoice_id', tags=['Invoice'], response_model=PayInvoiceResponseModel)
def pay_invoice(
        invoice_id: int,
        user = Depends(get_current_account),
):
    return mark_invoice_paid(
        user_id=user.user_id,
        invoice_id=invoice_id
    )






