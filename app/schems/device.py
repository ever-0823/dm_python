# Pydantic 是 FastAPI 的数据验证基石，几乎所有请求/响应数据都通过它来验证。
from typing import Literal

from pydantic import BaseModel, Field, field_validator

DeviceStatus = Literal["active", "inactive", "maintenance", "retired"]


# 这个类的作用是定义“设备数据长什么样”
class DeviceResponse(BaseModel):
    id: int
    device_id: str
    device_name: str
    model: str
    manufacturer: str
    location: str
    status: str


class DeviceCreateRequest(BaseModel):
    #为模型字段添加验证规则和元数据
    #Field:Pydantic的字段验证函数,...表示必填（不能省略）
    device_id: str = Field(..., min_length=1, max_length=50)
    device_name: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., max_length=100)
    manufacturer: str = Field(..., max_length=100)
    location: str = Field(..., max_length=100)
    status: DeviceStatus = "active"

    @field_validator("device_id", "device_name", "model", "manufacturer", "location")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class DeviceUpdateRequest(BaseModel):
    device_name: str = Field(..., min_length=1, max_length=100)
    model: str = Field("", max_length=100)
    manufacturer: str = Field("", max_length=100)
    location: str = Field("", max_length=100)
    status: DeviceStatus = "active"

    @field_validator("device_name", "model", "manufacturer", "location")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class DeviceBatchDeleteRequest(BaseModel):
    device_ids: list[str] = Field(..., min_length=1, max_length=100)

    @field_validator("device_ids")
    @classmethod
    def validate_device_ids(cls, value: list[str]) -> list[str]:
        cleaned = []
        for item in value:
            device_id = item.strip()
            if not device_id:
                raise ValueError("设备编号不能为空")
            cleaned.append(device_id)
        return cleaned
