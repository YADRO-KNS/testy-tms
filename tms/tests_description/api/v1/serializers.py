from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer
from tests_description.models import HistoricalTestCase, TestCase, TestSuite


class TestSuiteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testsuite-detail')

    class Meta:
        model = TestSuite
        fields = ('id', 'name', 'parent', 'project', 'level', 'lft', 'rght', 'tree_id', 'url')


class TestCaseSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:testcase-detail')

    class Meta:
        model = TestCase
        fields = ('id', 'name', 'project', 'suite', 'setup', 'scenario', 'teardown', 'estimate', 'url')


class HistoricalTestCaseSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:v1:historicaltestcase-detail')

    class Meta:
        model = HistoricalTestCase
        fields = ('id', 'history_user', 'project', 'suite', 'estimate', 'history_change_reason', 'history_date',
                  'history_type', 'id', 'name', 'scenario', 'setup', 'teardown', 'created_at', 'updated_at', 'url')
