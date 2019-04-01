# Stdlib imports

# Core Django imports

# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Imports from your apps
from .models import Shop
from .serializers import ShopSerializer, CreateShopSerializer


class ShopListView(APIView):
    """
    List all the shop information
    """
    def get(self, request):
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)


class ShopCreateView(APIView):
    def post(self, request):
        serializers = CreateShopSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
