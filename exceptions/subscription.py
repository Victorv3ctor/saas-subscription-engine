class InvalidSubscriptionPlan(Exception):
    pass

class SubscriptionDurationExceeded(Exception):
    pass

class NoSubscription(Exception):
    pass


class ActiveSubscription(Exception):
    pass