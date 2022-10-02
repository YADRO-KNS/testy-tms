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

    def user_update(self, user: UserModel, dto: UserDto) -> UserModel:
        user.username = dto.username
        user.first_name = dto.first_name
        user.last_name = dto.last_name
        user.email = dto.email
        user.is_staff = dto.is_staff
        user.is_active = dto.is_active
        user.set_password(dto.password)
        user.full_clean()
        user.save()
        return user

    def user_delete(self, user: UserModel):
        user.delete()
        return user

    def user_retrieve_all(self):
        return UserModel.objects.all()

    def user_retrieve_by_id(self, user_id):
        return UserModel.objects.get(pk=user_id)
