class InvalidSubscriptionPlan(Exception):
    detail='New subscription plan must be different'

class SubscriptionNotFound(Exception):
    pass


class ActiveSubscription(Exception):
    detail='YOU HAVE ACTIVE SUBSCRIPTION'
