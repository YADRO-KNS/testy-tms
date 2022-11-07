
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from users.api.v1.serializers import GroupSerializer, UserSerializer
from users.selectors.groups import GroupSelector
from users.selectors.users import UserSelector
from users.services.groups import GroupService
from users.services.users import UserService

UserModel = get_user_model()


class GroupViewSet(ModelViewSet):
    queryset = GroupSelector().group_list()
    serializer_class = GroupSerializer

    def perform_create(self, serializer: GroupSerializer):
        serializer.instance = GroupService().group_create(serializer.validated_data)

    def perform_update(self, serializer: UserSerializer):
        serializer.instance = GroupService().group_update(serializer.instance, serializer.validated_data)


class UserViewSet(ModelViewSet):
    queryset = UserSelector().user_list()
    serializer_class = UserSerializer

    def perform_create(self, serializer: UserSerializer):
        serializer.instance = UserService().user_create(serializer.validated_data)

    def perform_update(self, serializer: UserSerializer):
        serializer.instance = UserService().user_update(serializer.instance, serializer.validated_data)
