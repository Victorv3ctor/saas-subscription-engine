class Subscription:
    def __init__(
            self,user_id, status, plan, started_at, expires_at, canceled_at: None = None, sub_id: int | None = None
    ):
        self.user_id = user_id
        self.status = status #active inactive canceled
        self.plan = plan #low medium pro
        self.started_at = started_at
        self.expires_at = expires_at
        self.canceled_at = canceled_at
        self.sub_id = sub_id

    @classmethod
    def create(
            cls, user_id, plan, started_at, expires_at
    ):
        return cls(
            user_id = user_id,
            status='active',
            plan = plan,
            started_at=started_at,
            expires_at=expires_at
        )

    def is_active(self, date_now):
        return self.status=='active' and self.expires_at > date_now








