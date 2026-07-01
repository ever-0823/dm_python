from fastapi import APIRouter
from app.model.user import User

router = APIRouter()

@router.get("/users")
def get_users():
    users = User.get_all()
    return {
        "success": True,
        "data": users
    }