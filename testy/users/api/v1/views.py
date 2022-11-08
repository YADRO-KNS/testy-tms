# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.

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
