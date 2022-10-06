from rest_framework.serializers import (HyperlinkedIdentityField,
                                        ModelSerializer)

from core.models import Project

__all__ = (
    'ProjectSerializer'
)


class ProjectSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:project-detail')

    class Meta:
        model = Project
        fields = ('id', 'url', 'name', 'description')
