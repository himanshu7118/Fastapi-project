from pydantic import BaseModel

class LoginSchema(BaseModel):
    username: str = "username"
    password: str = "password"