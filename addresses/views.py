# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Imports from your apps
from .models import Address
from .serializers import AddressListSerializer, AddAddressSerializer


class GetAddressListView(APIView):
    """
    Get all the addresses of single customer
    input: id
    output: serializer
    """
    def post(self, request):
        address_list = Address.objects.filter(who=request.data.get('id'))
        serializer = AddressListSerializer(address_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetDefaultAddressView(APIView):
    """
    Set one as default address of single customer
    input:  id
            addId
    output: 202
    """
    def post(self, request):
        address_list = Address.objects.filter(who=request.data.get('id'))
        for add in address_list:
            if add.isDefault:
                add.isDefault = False
                add.save()
        address = Address.objects.get(pk=request.data.get('addId'))
        address.isDefault = True
        address.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class DeleteAddressView(APIView):
    """
    Delete one address of single customer
    input:  addId
    output: 204
    Note: if the delete address is the default address ?
    """
    def post(self, request):
        address = Address.objects.get(pk=request.data.get('addId'))
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddAddressView(APIView):
    """
    Add new address of single customer
    """
    def post(self, request):
        serializers = AddAddressSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
