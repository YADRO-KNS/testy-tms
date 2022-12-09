from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField, HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer

from testrail_migrator.models import TestrailSettings, TestrailBackup
from tests_representation.models import Parameter, Test
from tests_representation.selectors.results import TestResultSelector
from users.models import User


class ParameterSerializer(ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'project', 'data', 'group_name')


class TestrailSettingsInputSerializer(ModelSerializer):
    class Meta:
        model = TestrailSettings
        fields = ('login', 'password', 'api_url', 'dumpfile_path')


class TestrailSettingsOutputSerializer(ModelSerializer):
    class Meta:
        model = TestrailSettings
        fields = ('login', 'api_url', 'dumpfile_path')


class TestrailUploadSerializer(serializers.Serializer):
    testrail_backup = PrimaryKeyRelatedField(queryset=TestrailBackup.objects.all())
    user = PrimaryKeyRelatedField(queryset=User.objects.all())


class DownloadSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    create_dumpfile = serializers.BooleanField()
    testrail_settings = PrimaryKeyRelatedField(queryset=TestrailSettings.objects.all())


class TestrailBackupSerializer(ModelSerializer):
    class Meta:
        model = TestrailBackup
        fields = ('name', 'filepath')

class TestSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:test-detail')
    name = SerializerMethodField(read_only=True)
    last_status = SerializerMethodField(read_only=True)

    class Meta:
        model = Test
        fields = (
            'id', 'project', 'case', 'name', 'last_status', 'plan', 'user', 'is_archive', 'created_at', 'updated_at',
            'url')

    def get_name(self, instance):
        return instance.case.name

    def get_last_status(self, instance):
        result = TestResultSelector().last_result_by_test_id(instance.id)
        if result:
            return result.get_status_display()