from typing import Any, Dict, List
from pydantic import BaseModel


class PaginationParams(BaseModel):
    """Pagination parameters for API requests."""
    skip: int = 0
    limit: int = 100
    
    model_config = {"from_attributes": True}


class PaginationResponse(BaseModel):
    """Pagination response model."""
    items: List[Any]
    total: int
    page: int
    per_page: int
    total_pages: int
    
    model_config = {"from_attributes": True}


def paginate(
    items: List[Any], 
    skip: int = 0, 
    limit: int = 100, 
    total: int = 0
) -> Dict[str, Any]:
    """Paginate a list of items."""
    total_pages = (total + limit - 1) // limit if total else 1
    return {
        "items": items[skip:skip + limit],
        "total": total,
        "page": (skip // limit) + 1,
        "per_page": limit,
        "total_pages": total_pages,
    }