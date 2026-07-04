from datetime import datetime, timedelta
from exceptions.subscription import InvalidSubscriptionPlan

class Subscription:
    def __init__(
            self,user_id, plan, started_at, expires_at, canceled_at: None = None, sub_id: int | None = None
    ):
        self.user_id = user_id
        self.plan = plan #silver/gold/platinum
        self.started_at = started_at
        self.expires_at = expires_at
        self.canceled_at = canceled_at
        self.sub_id = sub_id

    @classmethod
    def create(
            cls, user_id, plan, duration
    ):
        return cls(
            user_id = user_id,
            plan = plan,
            started_at=datetime.now().date(),
            expires_at=datetime.now().date() + timedelta(days=duration)
        )

    def is_active(self):
        now = datetime.now().date()
        return (
                self.canceled_at is None and
                self.started_at <= now < self.expires_at
        )

    def cancel(self):
        self.canceled_at=datetime.now().date()

    def ensure_can_change_plan(self, data_plan):
        if self.plan == data_plan:
            raise InvalidSubscriptionPlan()










