from pydantic import BaseModel, Field
from typing import Optional


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: Optional[str] = Field(max_length=255)
    priority: str = Field(min_length=1, max_length=10)
    completed: int = Field(default=0, ge=0, le=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Todo Title",
                "description": "Todo Description",
                "priority": "High",
                "completed": 0
            }
        }
    }
