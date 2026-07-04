from pydantic import BaseModel, Field, ConfigDict

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3)
    email: str
    pwd: str

class LoginRequest(BaseModel):
    username: str
    pwd: str

class RegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    email: str