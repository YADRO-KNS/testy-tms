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
from core.api.v1.serializers import AttachmentSerializer
from core.selectors.attachments import AttachmentSelector
from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from tests_description.models import TestCase, TestSuite


class TestCaseSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testcase-detail')
    key = IntegerField(source='id', read_only=True)
    value = IntegerField(source='id', read_only=True)
    attachments = PrimaryKeyRelatedField(
        many=True, queryset=AttachmentSelector().attachment_list(), required=False
    )

    class Meta:
        model = TestCase
        fields = (
            'id', 'key', 'value', 'name', 'project', 'attachments', 'suite', 'setup', 'scenario', 'teardown',
            'estimate', 'url'
        )


class TestCaseRetrieveSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testcase-detail')
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = TestCase
        fields = ('id', 'name', 'project', 'attachments', 'suite', 'setup', 'scenario', 'teardown', 'estimate', 'url')


class TestSuiteTreeSerializer(ModelSerializer):
    children = SerializerMethodField()
    key = serializers.IntegerField(source='id')
    value = serializers.IntegerField(source='id')
    title = serializers.CharField(source='name')
    descendant_count = SerializerMethodField()

    class Meta:
        model = TestSuite
        fields = ('id', 'value', 'name', 'key', 'title', 'level', 'children',
                  'descendant_count',
                  )

    def get_descendant_count(self, instance):
        return instance.get_descendant_count()

    def get_children(self, value):
        return self.__class__(value.child_test_suites.all(), many=True).data


class TestSuiteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testsuite-detail')
    test_cases = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        model = TestSuite
        fields = ('id', 'name', 'parent', 'project', 'url', 'test_cases',)
