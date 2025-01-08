from fastapi import APIRouter
from schemas.combined import search_all_content

router = APIRouter()

@router.get("/{query}",
    summary="Search All Content",
    description="Search both products and videos across all categories."
)
async def search_all_content_(query: str):
    return await search_all_content(query)