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
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer
from tests_description.models import TestCase, TestSuite


class TestCaseSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testcase-detail')

    class Meta:
        model = TestCase
        fields = ('id', 'name', 'project', 'suite', 'setup', 'scenario', 'teardown', 'estimate', 'url')


class TestCaseRetrieveSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testcase-detail')
    attachments = SerializerMethodField()

    class Meta:
        model = TestCase
        fields = ('id', 'name', 'project', 'attachments', 'suite', 'setup', 'scenario', 'teardown', 'estimate', 'url')

    def get_attachments(self, obj):
        serializer_context = {'request': self.context.get('request')}
        attachments = AttachmentSelector().attachment_list_by_parent_object(TestCase, obj.id)
        serializer = AttachmentSerializer(attachments, many=True, context=serializer_context)
        return serializer.data


class TestSuiteTreeSerializer(ModelSerializer):
    children = SerializerMethodField()
    test_cases = SerializerMethodField('get_test_case_serializer')
    key = serializers.IntegerField(source='id')
    value = serializers.IntegerField(source='id')
    title = serializers.CharField(source='name')

    class Meta:
        model = TestSuite
        fields = ('id', 'value', 'name', 'key', 'title', 'level', 'children', 'test_cases')

    def get_children(self, value):
        return self.__class__(value.get_children(), many=True).data

    def get_test_case_serializer(self, obj):
        serializer_context = {'request': self.context.get('request')}
        test_cases = TestCase.objects.all().filter(suite=obj)
        serializer = TestCaseSerializer(test_cases, many=True, context=serializer_context)
        return serializer.data


class TestSuiteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testsuite-detail')
    test_cases = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        model = TestSuite
        fields = ('id', 'name', 'parent', 'project', 'url', 'test_cases',)
