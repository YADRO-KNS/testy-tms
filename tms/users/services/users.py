from typing import Any, Dict

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserService:
    non_side_effect_fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']

    def user_create(self, data: Dict[str, Any]) -> UserModel:
        user = UserModel.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=False,
        )
        user.set_password(data['password'])
        user.full_clean()
        user.save()
        return user

    def user_update(self, user: UserModel, data: Dict[str, Any]) -> UserModel:
        user, _ = user.model_update(
            fields=self.non_side_effect_fields,
            data=data,
            commit=False,
        )
        password = data.pop('password', None)
        if password:
            user.set_password(password)
        user.full_clean()
        user.save()
        return user
