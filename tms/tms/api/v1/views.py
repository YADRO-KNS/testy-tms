from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import APIRootView


class V1RootView(APIRootView):
    def get_view_name(self):
        return 'v1'

    def get(self, request, format=None):
        return Response({
            'projects': reverse('api:v1:project-list', request=request, format=format),
            'suites': reverse('api:v1:testsuite-list', request=request, format=format),
            'cases': reverse('api:v1:testcase-list', request=request, format=format),
            'historical_cases': reverse('api:v1:historicaltestcase-list', request=request, format=format),
            'plans': reverse('api:v1:testplan-list', request=request, format=format),
            'tests': reverse('api:v1:test-list', request=request, format=format),
            'results': reverse('api:v1:testresult-list', request=request, format=format),
            'parameters': reverse('api:v1:parameter-list', request=request, format=format),
            'statuses': reverse('api:v1:teststatus-list', request=request, format=format),
            'users': reverse('api:v1:users-api:api-root', request=request, format=format),
        })
