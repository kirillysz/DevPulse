from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str = Field(..., description="JWT token string")
    token_type: str = Field(..., description="Type of the token")
