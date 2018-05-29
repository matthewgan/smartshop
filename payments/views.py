# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Imports from your apps


class GetTencentNotifyView(APIView):
    def post(self, request):
        if request.data.get('return_code') == 'SUCCESS':
            res = {'return_code': 'SUCCESS', 'return_msg': ''}
            return Response(res, status=status.HTTP_200_OK)
