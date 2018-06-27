# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
# Imports from your apps
from customers.models import Customer
from customers.serializers import EntranceGetInfoRequestSerializer, EntranceGetInfoResponseSerializer


class EntranceGetUserInfoView(APIView):
    def post(self, request):
        serializer = EntranceGetInfoRequestSerializer(data=request.data)
        if serializer.is_valid():
            wuser = Customer.objects.get(code=serializer.data.get('code'))
            output_serializer = EntranceGetInfoResponseSerializer(wuser)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
