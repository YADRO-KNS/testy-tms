import asyncio

from rest_framework.views import APIView

from tests_description.models import TestCase, TestSuite
from tests_representation.models import TestPlan, Test, TestResult, Parameter
from .entrypoint_cli import main, upload_to_testy
from rest_framework.response import Response


# TODO: remove after debugging is finished
class ClearView(APIView):
    def get(self, request):
        TestPlan.objects.all().delete()
        Test.objects.all().delete()
        TestResult.objects.all().delete()
        TestCase.objects.all().delete()
        TestSuite.objects.all().delete()
        Parameter.objects.all().delete()
        return Response('123')


class UploaderView(APIView):

    def get(self, request):
        # asyncio.run(main())
        try:
            upload_to_testy(1)
        except Exception as err:
            raise err

        # TODO: remove after debugging is finished
        return Response('123')
