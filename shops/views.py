# Stdlib imports

# Core Django imports

# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response

# Imports from your apps
from .models import Shop
from .serializers import ShopSerializer


class ShopListView(APIView):
    """
    List all the shop information
    """
    def get(self, request):
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)
