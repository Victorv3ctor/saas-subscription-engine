from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3)
    email: str
    pwd: str

class LoginRequest(BaseModel):
    username: str
    pwd: str

class SubscriptionRequest(BaseModel):
    plan: str = Field(description='LOW/MEDIUM/PRO')
    long_term: int  = Field(description='7/14/31/364')

class ChangeSubscriptionPlan(BaseModel):
    new_plan: str = Field(description='LOW/MEDIUM/PRO')
    new_duration: int = Field(description='7/14/31/364')