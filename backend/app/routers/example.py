from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_example():
    return {"message": "This is an example route."}