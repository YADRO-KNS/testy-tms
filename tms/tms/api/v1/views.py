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
            'tests': reverse('api:v1:test-list', request=request, format=format),
            'results': reverse('api:v1:testresult-list', request=request, format=format),
            'parameters': reverse('api:v1:parameter-list', request=request, format=format),
            'users': reverse('api:v1:user-list', request=request, format=format),
            'groups': reverse('api:v1:group-list', request=request, format=format),
            'attachments': reverse('api:v1:attachment-list', request=request, format=format)
        })
