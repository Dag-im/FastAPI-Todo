from pydantic import BaseModel, Field
from typing import Optional, List

class TodoItem(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: bool = False

    class Config:
        from_attributes = True

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

    class Config:
        from_attributes = True

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None

    class Config:
        from_attributes = True

class TodoListResponse(BaseModel):
    todos: List[TodoItem]

    class Config:
        from_attributes = True
