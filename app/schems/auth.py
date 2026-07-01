from pydantic import BaseModel, Field, field_validator

"""
这是一个使用 Pydantic 定义的数据验证模型，用于在 FastAPI 中接收和验证客户端发送的请求数据。
"""


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)  # 必填，必须是字符串类型
    password: str = Field(..., min_length=3, max_length=100)

    role: str = "user"  # 可选，默认值为 "user"

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("用户不能为空")
        return value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("角色只能是user或admin")
        return value


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=3, max_length=100)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("用户不能为空")
        return value
