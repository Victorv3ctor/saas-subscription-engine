from pydantic import BaseModel, Field, ConfigDict
from typing import Literal
from datetime import datetime

class SubscriptionRequest(BaseModel):
    plan: Literal['silver', 'gold', 'platinum']
    duration: Literal[7, 14, 30, 364]

class ChangeSubscriptionRequest(BaseModel):
    plan: Literal['silver', 'gold', 'platinum']
    duration: Literal[7, 14, 30, 364]


class CancelSubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sub_id: int
    canceled_at: datetime

class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sub_id: int
    plan: str
    started_at: datetime
    expires_at: datetime




