#EXCEPTIONS USER
from exceptions.user import (
    WrongPassword,
    UsernameNotFound)

#EXCEPTIONS SUBSCRIPTION
from exceptions.subscription import (
    InvalidSubscriptionPlan,
    SubscriptionDurationExceeded,
    NoSubscription,
    ActiveSubscription)

#DOMAIN MODELS
from models.subscription import Subscription
from models.user import User
from models.invoice import Invoice
#LIBRARIES
from datetime import datetime, timedelta
import bcrypt

class Service:
    def __init__(self, repo):
        self.repo = repo

#SUBSCRIPTION validation
    @staticmethod
    def long_term_input_validation(long_term):
        duration = [7, 14, 31, 364]
        if long_term not in duration:
            raise SubscriptionDurationExceeded()
        return long_term

#SUBSCRIPTION validation
    @staticmethod
    def plan_input_validation(plan):
        if plan not in ['low', 'medium', 'pro']:
            raise InvalidSubscriptionPlan()
        return plan

#QUERY + VALID - service layer is responsible for selecting business-relevant state
    def get_active_sub(self, user_id):
        subs = self.repo.get_subs_by_user_id(user_id)
        date_now = datetime.now().date()
        active = next(
            (s for s in subs if s.is_active(date_now)),
            None
        )
        return active

    def get_active_invoice(self, user_id):
        invoices = self.repo.get_invoices_by_user_id(user_id)

        date_now = datetime.now().date()

        active = next(
            (i for i in invoices if i.is_active(date_now)),
            None
        )
        return active

#GUARDS
    def assert_not_active_sub(self, user_id):
        active = self.get_active_sub(user_id)
        if active:
            raise ActiveSubscription()

    def assert_active_sub(self, user_id):
        active = self.get_active_sub(user_id)
        if not active:
            raise NoSubscription()
        return active


#SUBSCRIPTION FLOW WRITE/READ
    def new_sub(self, user_id, plan, long_term):
        self.assert_not_active_sub(user_id)
        plan = self.plan_input_validation(plan)
        long_term = self.long_term_input_validation(long_term)
        started_at = datetime.now().date()
        expires_at = started_at + timedelta(days=long_term)
        sub = Subscription.create(user_id, plan, started_at, expires_at)
        self.repo.save_subscription(sub)
        invoice = Invoice.create(
            user_id=user_id,
            sub_id=sub.sub_id,
            sub_plan=sub.plan,
            issued_at=started_at
        )
        self.repo.save_invoice(invoice)

    def change_current_sub(self, user_id, new_plan, new_duration):
        sub = self.assert_active_sub(user_id)
        plan = self.plan_input_validation(new_plan)
        long_term = self.long_term_input_validation(new_duration)
        invoice = self.get_active_invoice(user_id)
        sub.change_plan(
            new_plan=plan,
            new_duration = datetime.now().date() + timedelta(days=long_term)
        )
        invoice.update(new_plan=plan)
        self.repo.update_subscription(sub)
        self.repo.update_invoice(invoice)
        return sub

    def cancel_sub(self, user_id):
        sub = self.assert_active_sub(user_id)
        invoice = self.get_active_invoice(user_id)
        canceled_at = datetime.now().date()
        sub.cancel(canceled_at)
        invoice.cancel(canceled_at)
        self.repo.expire_subscription(sub)
        self.repo.expire_invoice(invoice)

    def sub_status(self, user_id):
        sub = self.get_active_sub(user_id)

        if not sub:
            return {
                "has_subscription": False
            }

        return {
            "has_subscription": True,
            "subscription":{
                "status": sub.status,
                "plan": sub.plan,
                "expiration": sub.expires_at
            }
        }

#INVOICE READ
    def invoice_status(self, user_id):
        invoice = self.get_active_invoice(user_id)

        if not invoice:
            return {
                "has_invoice": False
            }

        return {
            "has_invoice": True,
            "invoice": {
                "status": invoice.status,
                "sub_plan" : invoice.sub_plan,
                "amount": invoice.amount,
                "expiration": invoice.expires_at,
                "invoice_number": invoice.invoice_id
            }
        }

#USER READ
    def profile_status(self, user_id):
        user = self.repo.get_user_by_id(user_id)
        sub = self.sub_status(user_id)
        invoice = self.invoice_status(user_id)
        return {
            'username': user.username,
            'email': user.email,
            'subscription': sub,
            'invoice': invoice
        }

#USER FLOW
    def new_user(self, data_username, data_password, data_email):
        hashed_data_pwd = bcrypt.hashpw(data_password.encode('utf-8'), bcrypt.gensalt())
        str_hashed_data_pwd = hashed_data_pwd.decode('utf-8')
        user = User.create(data_username, str_hashed_data_pwd, data_email)
        self.repo.save_user(user)


    def check_user_credentials(self, data_username, data_pwd):
        user = self.repo.get_user_by_username(data_username)
        if user is None:
            raise UsernameNotFound()

        if not bcrypt.checkpw(data_pwd.encode('utf-8'), user.pwd.encode('utf-8')):
            raise WrongPassword()

        return user






















