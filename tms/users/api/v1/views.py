from django.contrib.auth import get_user_model
from rest_framework.routers import APIRootView
from rest_framework.viewsets import ModelViewSet
from users.api.v1.serializers import UserSerializer
from users.selectors.users import UserSelector
from users.services.users import UserService

UserModel = get_user_model()


class UsersRootView(APIRootView):
    """
    Users API root view
    """

    def get_view_name(self) -> str:
        return 'Users'


class UserViewSet(ModelViewSet):
    queryset = UserSelector().user_list()
    serializer_class = UserSerializer

    def perform_create(self, serializer: UserSerializer):
        serializer.instance = UserService().user_create(serializer.validated_data)

    def perform_update(self, serializer: UserSerializer):
        serializer.instance = UserService().user_update(serializer.instance, serializer.validated_data)
