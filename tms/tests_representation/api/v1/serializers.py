from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer
from tests_representation.models import Attachment, Parameter, Test, TestResult


class ParameterSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:parameter-detail')

    class Meta:
        model = Parameter
        fields = ('id', 'project', 'data', 'group_name', 'url')


class TestSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:test-detail')

    class Meta:
        model = Test
        fields = ('id', 'project', 'case', 'plan', 'user', 'is_archive', 'created_at', 'updated_at', 'url')

        read_only_fields = ('project',)


class TestResultSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testresult-detail')

    class Meta:
        model = TestResult
        fields = (
            'id', 'project', 'status', 'test', 'user', 'comment', 'is_archive', 'test_case_version', 'created_at',
            'updated_at', 'url'
        )

        read_only_fields = ('test_case_version', 'project', 'test')


class AttachmentSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:attachment-detail')

    class Meta:
        model = Attachment
        fields = ('project', 'name', 'filename', 'content_type', 'size', 'case', 'result', 'user', 'file', 'url')

        # read_only_fields = ('project',)
