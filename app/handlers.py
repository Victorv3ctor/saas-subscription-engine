from fastapi.responses import JSONResponse

from exceptions.user import UsernameNotFound, WrongPassword, UsernameExists, EmailExists

from exceptions.subscription import (
    InvalidSubscriptionPlan,
    SubscriptionDurationExceeded, NoSubscription,
    ActiveSubscription)

#USER HANDLERS
def register_exception_handlers(app):

    @app.exception_handler(UsernameExists)
    def handle_username_exists(request_obj, exc_obj):

        return JSONResponse(
            status_code=400,
            content = {
                'detail': 'USERNAME EXISTS'
            }
        )

    @app.exception_handler(EmailExists)
    def handle_email_exists(request_obj, exc_obj):
        return JSONResponse(
            status_code=409,
            content = {
                'detail': 'USER WITH THIS EMAIL EXISTS'
            }
        )

def login_in_exception_handler(app):

    @app.exception_handler(UsernameNotFound)
    def handle_wrong_username(req_obj, exc_obj):
        return JSONResponse(
            status_code=401,
            content = {
                'details': 'WRONG USERNAME/PASSWORD'
            }
        )

    @app.exception_handler(WrongPassword)
    def handle_wrong_password(request_obj, exc_obj):
        return JSONResponse(
            status_code=401,
            content = {
                'detail': 'WRONG USERNAME / PASSWORD'
            }
        )

#SUBSCRIPTION HANDLERS
def subscription_exceptions_handler(app):

    @app.exception_handler(ActiveSubscription)
    def handle_sub_exist(req_obj, exc_obj):
        return JSONResponse(
            status_code=409,
            content = {
                'detail': 'YOUR SUBSCRIPTION IS ACTIVE'
            }
        )

    @app.exception_handler(InvalidSubscriptionPlan)
    def handle_invalid_subscription_plan(req_obj, exc_obj):
        return JSONResponse(
            status_code=404,
            content = {
                'detail': 'CHOOSE LOW/MEDIUM/PRO PLAN'
            }
        )

    @app.exception_handler(SubscriptionDurationExceeded)
    def handle_subscription_duration(request_obj, exc_obj):
        return JSONResponse(
            status_code = 404,
            content = {
                'detail': 'CHOOSE SUB DURATION(DAYS): 7/14/31/364'
            }
        )

    @app.exception_handler(NoSubscription)
    def handle_no_subscription(req_obj, exc_obj):
        return JSONResponse(
            status_code = 404,
            content = {
                'detail': 'YOU HAVE NOT ACTIVE SUBSCRIPTION'
            }
        )






