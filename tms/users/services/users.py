from dataclasses import dataclass

from django.contrib.auth import get_user_model

UserModel = get_user_model()


@dataclass
class UserDto:
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    is_staff: bool
    is_active: bool


class UserService:
    def user_create(self, dto: UserDto) -> UserModel:
        user = UserModel(
            username=dto.username,
            first_name=dto.first_name,
            last_name=dto.last_name,
            email=dto.email,
            is_staff=dto.is_staff,
            is_active=dto.is_active
        )
        user.set_password(dto.password)
        user.full_clean()
        user.save()
        return user
