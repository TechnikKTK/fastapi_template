from pydantic import BaseModel, Field


class ApiResponseStatus(BaseModel):
    code: int = Field(description="Status code")
    message: str = Field(description="Response message")


class ApiResponseSchema(BaseModel):
    status: ApiResponseStatus
