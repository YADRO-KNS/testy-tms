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
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from testrail_migrator.models import TestrailBackup, TestrailSettings
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
    testrail_settings = PrimaryKeyRelatedField(queryset=TestrailSettings.objects.all())
    upload_root_runs = serializers.BooleanField(default=False)


class DownloadSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    download_attachments = serializers.BooleanField(default=True)
    ignore_completed = serializers.BooleanField(default=True)
    testrail_settings = PrimaryKeyRelatedField(queryset=TestrailSettings.objects.all())
    backup_filename = serializers.CharField(default='testrail_backup')


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
