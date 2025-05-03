from typing import List, TypeVar, Generic
from pydantic import BaseModel
T = TypeVar('T')
class PaginationResponse(BaseModel, Generic[T]):
    items: List[T]
    total_items: int
    total_pages: int
    current_page: int
    per_page: int
    
    class Config:
        from_attributes = True