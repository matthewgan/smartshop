# Stdlib imports

# Core Django imports

# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Imports from your apps
from .models import Category
from .serializers import CategorySerializer


class CategoryListView(APIView):
    """
    List all the categories in the database: ids & names
    miniApp-shop.js

    Parameters:

    Returns:
      all Category Info

    Raises:
    """
    def get(self, request):
        category = Category.objects.all()
        output_serializer = CategorySerializer(category, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

