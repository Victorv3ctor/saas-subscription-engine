from datetime import timedelta

class Invoice:
    def __init__(
            self,
            user_id,
            sub_id,
            status, #pending paid canceled, expired
            sub_plan,
            issued_at,
            amount,
            currency,
            expires_at,
            canceled_at: None = None,
            invoice_id: None = None
    ):
        self.user_id = user_id
        self.sub_id = sub_id
        self.status = status
        self.sub_plan = sub_plan
        self.issued_at = issued_at
        self.amount = amount
        self.currency = currency
        self.expires_at = expires_at
        self.canceled_at = canceled_at
        self.invoice_id = invoice_id


    @classmethod
    def create(cls,
               user_id, sub_id, sub_plan, issued_at
               ): #dni

        return cls(
            user_id=user_id,
            sub_id=sub_id,
            status='pending',
            sub_plan=sub_plan,
            issued_at=issued_at,
            amount=40,
            currency='USD',
            expires_at = issued_at + timedelta(days=30)
        )

    def is_active(self, date_now):
        return self.status=='pending' and self.expires_at > date_now






