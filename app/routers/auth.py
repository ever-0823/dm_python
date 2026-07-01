
from ..core.auth import TokenStore, extract_bearer_token
from ..core.responses import success_response
from ..model.login import verify_password
from ..model.user import User
from fastapi import APIRouter, Depends,Header
from ..core.security import hash_password
from ..schems.auth import RegisterRequest
from ..dependencies.auth import current_user
from ..core.exceptions import AppException

router = APIRouter()
"""
注册用户
payload: RegisterRequest  自动验证请求体，符合模型则通过
"""


@router.post("/auth/register")
def register(payload: RegisterRequest):
    existing = User.find_by_username(payload.username)
    if existing:
        raise AppException(400,"用户名已存在")
    user_id = User.create(
        payload.username,
        hash_password(payload.password),
        payload.role
    )
    # return {"success": True, "user_id": user_id}
    return success_response(
        message="注册成功",
        user_id=user_id,
    )

"""登录"""


@router.post("/auth/login")
def login(payload: RegisterRequest):
    user = User.find_by_username(payload.username)
    if not user:
        raise AppException(401,"用户名或密码错误")
    if not verify_password(payload.password, user["password_hash"]):
        raise AppException(401,"用户名或密码错误")

    token = TokenStore.create_token(user)

    # return {"success": True, "message": "登陆成功",
    #         "access_token": token,  # 新增token
    #         "token_type": "bearer",  # token类型
    #         "user": {
    #             "id": user["id"],
    #             "username": user["username"],
    #             "role": user["role"],
    #             "created_at": user["created_at"],
    #         }, }
    return success_response(
        message="登录成功",
        data={
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
                "created_at": user["created_at"],
            },
        },
    )


@router.get("/auth/me")
def me(user=Depends(current_user)):
    """
    获取当前登录用户信息。
    只有带着合法 token 才能访问。
    """
    return success_response(data=user)

"""
Header(default=None)：从请求头里拿 Authorization
extract_bearer_token(...)：把 Bearer xxx 里的 xxx 取出来
TokenStore.revoke_token(...)：删除这个 token，让它失效
"""
@router.post("/auth/logout")
def logout(authorization: str | None = Header(None)):
    print(f"authorization:{authorization}")
    # token = TokenStore.create_token(authorization)
    token = extract_bearer_token(authorization)
    print(f"token被移除:{token}")
    TokenStore.revoke_token(token)
    # return {"success": True, "message": "退出成功"}
    return success_response(message="退出成功")