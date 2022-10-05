from django.contrib.auth import get_user_model
from django.db.models import QuerySet

UserModel = get_user_model()


class UserSelector:
    def user_list(self) -> QuerySet[UserModel]:
        return QuerySet(model=UserModel).prefetch_related('groups').order_by('username')
