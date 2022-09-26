from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.routers import APIRootView
from rest_framework.viewsets import ModelViewSet

from tms.utils.mixins import DtoMixin
from users.api.v1.serializers import UserSerializer
from users.services.users import UserDto, UserService

UserModel = get_user_model()


class UsersRootView(APIRootView):
    """
    Users API root view
    """

    def get_view_name(self) -> str:
        return 'Users'


class UserViewSet(ModelViewSet, DtoMixin):
    queryset = QuerySet(model=UserModel).prefetch_related('groups').order_by('username')
    serializer_class = UserSerializer
    dto_class = UserDto

    def perform_create(self, serializer: UserSerializer):
        dto = self.build_dto_from_validated_data(serializer.validated_data)
        serializer.instance = UserService().user_create(dto)
