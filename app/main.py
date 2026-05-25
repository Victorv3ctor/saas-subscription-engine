#LIBRARIES
from fastapi import FastAPI, Depends
from schemas.schemas import RegisterRequest, LoginRequest, SubscriptionRequest, ChangeSubscriptionPlan

#SERVICE DOMAIN
from service.service import Service

#SERVICE DEPENDENCIES
from dependencies.get_service import get_service

#AUTH
from service.auth import create_token
from service.auth import get_current_account

#EXCEPTIONS HANDLERS
from app.handlers import register_exception_handlers
from app.handlers import login_in_exception_handler
from app.handlers import subscription_exceptions_handler

app = FastAPI()

register_exception_handlers(app)
login_in_exception_handler(app)
subscription_exceptions_handler(app)

@app.post('/register')
def register(
        data: RegisterRequest,
        service: Service=Depends(get_service)
):
    service.new_user(
        data.username,
        data.pwd, data.email
        )
    return {
        'MSG': 'Account Registered',
        'NEXT_STEP': 'LogIn'
    }

@app.post('/login')
def login(
        data: LoginRequest,
        service: Service=Depends(get_service)
):
    user = service.check_user_credentials(data.username, data.pwd)
    token = create_token(user_id=user.user_id)
    return {
        'MSG': 'Logged In',
        'TOKEN': token
    }

@app.post('/upgrade/subscription')
def upgrade_sub(
        data: SubscriptionRequest,
        user = Depends(get_current_account),
        service: Service=Depends(get_service)
):
    service.new_sub(
        user.user_id,
        data.plan,
        data.long_term
    )
    return {
        'STATUS': 'OK',
        'MSG': 'SUB UPGRADED',
        'PLAN': data.plan,
        'DURATION(days)': data.long_term
    }

@app.get('/subscription')
def subscription_status(
        user=Depends(get_current_account),
        service: Service=Depends(get_service)
):
    return service.sub_status(user_id=user.user_id)

@app.post('/cancel/subscription')
def cancel_subscription(
        user = Depends(get_current_account),
        service: Service=Depends(get_service)
):
    service.cancel_sub(user_id=user.user_id)
    return {
        'STATUS': 'OK',
        'MSG': 'SUBSCRIPTION CANCELED'
    }

@app.get('/me')
def my_status(
        user=Depends(get_current_account),
        service: Service=Depends(get_service)
):
    return service.profile_status(user.user_id)

@app.patch('/subscription')
def change_current_subscription(
        data: ChangeSubscriptionPlan,
        user = Depends(get_current_account),
        service: Service=Depends(get_service)
):
    sub = service.change_current_sub(user.user_id, data.new_plan, data.new_duration)
    return {
        'STATUS': 'OK',
        'MSG': 'SUBSCRIPTION PLAN CHANGED',
        'NEW PLAN': sub.plan,
        'DURATION': sub.expires_at
    }






