from database.transaction import transaction
from domains.subscription import Subscription
from domains.invoice import Invoice
from exceptions.subscription import ActiveSubscription, SubscriptionNotFound
from services.invoice_service import cancel_invoice
from repository.repository import(
    get_subs_list_by_user_id, save_subscription,
    expire_subscription, save_invoice
)
#SERVICE

def get_subscription(conn, user_id):
    subscriptions = get_subs_list_by_user_id(conn, user_id)
    subscription = next(
        (sub for sub in subscriptions if sub.is_active())
        , None
    )
    return subscription

def set_new_subscription(user_id, data_plan, data_duration):
    with transaction() as conn:
        subscription = get_subscription(conn, user_id)
        if subscription:
            raise ActiveSubscription()

        subscription = Subscription.create(
            user_id=user_id,
            plan=data_plan,
            duration=data_duration
        )
        save_subscription(conn, subscription)

        invoice = Invoice.create(
            subscription_id=subscription.sub_id
            )

        save_invoice(conn, invoice)

        return subscription

def sub_inv_cancellation(conn, subscription):
    subscription.cancel()
    expire_subscription(conn, subscription)
    cancel_invoice(conn, sub_id=subscription.sub_id)
    return subscription

def subscription_and_inv_cancel(user_id):
    with transaction() as conn:
        subscription = get_subscription(conn, user_id)
        if not subscription:
            raise SubscriptionNotFound()

        return sub_inv_cancellation(conn, subscription)

def change_current_sub(user_id, data_plan, data_duration):
    with transaction() as conn:
        subscription = get_subscription(conn, user_id)
        if not subscription:
            raise SubscriptionNotFound()

        subscription.ensure_can_change_plan(data_plan)

        sub_inv_cancellation(conn, subscription)

        new_subscription = Subscription.create(
            user_id=user_id,
            plan=data_plan,
            duration=data_duration
        )

        save_subscription(conn, new_subscription)

        new_invoice = Invoice.create(
            subscription_id=new_subscription.sub_id
        )
        save_invoice(conn, new_invoice)

        return new_subscription


def subscription_query(user_id):
    with transaction() as conn:
        subscription = get_subscription(conn, user_id)
        if not subscription:
            raise SubscriptionNotFound()
        return subscription