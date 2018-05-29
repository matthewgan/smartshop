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
    Get addresslist
    miniApp-address.js

    Parameters:
        id - user id

    Returns:
      All addressInfo in list

    Raises:
    """
    def post(self, request):

        addressList = Address.objects.filter(who=request.data.get('id'))
        serializer = AddressListSerializer(addressList, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SetDefaultAddressView(APIView):
    """
    Set selected address to default
    miniApp-address.js

    Parameters:
        id - user id
        addId - address id

    Returns:
      'ok' - set success

    Raises:
    """
    def post(self, request):

        addList = Address.objects.filter(who=request.data.get('id'))
        for add in addList:
            if add.isDefault:
                add.isDefault = False
                add.save()

        address = Address.objects.get(id=request.data.get('addId'))
        address.isDefault = True
        address.save()

        return Response("ok", status=status.HTTP_200_OK)


class DeleteAddressView(APIView):
    """
    Delete selected address
    miniApp-address.js

    Parameters:
        addId - address id

    Returns:
      'ok' - delete success

    Raises:
    """
    def post(self, request):

        address = Address.objects.get(id=request.data.get('addId'))
        address.delete()

        return Response("ok", status=status.HTTP_200_OK)


class AddAddressView(APIView):
    """
    Add new address
    miniApp-add-address.js

    Parameters:
        who - user uuid
        name - add'name
        telephone -
        province -
        city -
        detail -

    Returns:
      'ok' - add success
      'dataerror' - request data error

    Raises:
    """
    def post(self, request):

        serializers = AddAddressSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response("ok", status=status.HTTP_200_OK)

        return Response("dataerror", status=status.HTTP_200_OK)