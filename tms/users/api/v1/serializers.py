from django.contrib.auth import get_user_model
from rest_framework.serializers import (HyperlinkedIdentityField,
                                        ModelSerializer)

UserModel = get_user_model()


class UserSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:users-api:user-detail')

    class Meta:
        model = UserModel
        fields = (
            'id', 'url', 'username', 'password', 'first_name', 'last_name', 'email', 'is_staff', 'is_active',
            'date_joined',
        )

        extra_kwargs = {
            'password': {'write_only': True}
        }
