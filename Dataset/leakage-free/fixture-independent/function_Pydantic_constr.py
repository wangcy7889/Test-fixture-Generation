from pydantic import BaseModel, EmailStr, ValidationError
from typing import Annotated

# 使用 Annotated 声明带有约束的类型
UsernameType = Annotated[str, 
                         dict(min_length=3, max_length=20, regex=r'^[a-zA-Z0-9_]+$')]

class UserProfile(BaseModel):
    username: UsernameType  # 使用定义好的类型
    email: EmailStr  # 确保是有效的电子邮件格式

def create_user_profile(username: str, email: str):
    try:
        profile = UserProfile(username=username, email=email)
        return profile
    except ValidationError as e:
        return e.errors()  # 如果数据无效，返回错误信息
