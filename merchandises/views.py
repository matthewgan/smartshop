# Stdlib imports

# Core Django imports
from django.http import Http404

# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Imports from your apps
from .models import Merchandise
from .serializers import MerchandiseListShowInfoSerializer
from .serializers import QueryMerchandiseDetailByBarcodeRequestSerializer, QueryMerchandiseDetailByBarcodeResponseSerializer
from .serializers import AddMerchandiseDetailByBarcodeSerializer


class MerchandisesShowByCategoryView(APIView):
    """
    List all the merchandises under specified category
    miniApp-shop.js

    Parameters:

    Returns:
      all Merchandises in specified category

    Raises:
    """
    def get_object(self, pk):
        try:
            return Merchandise.objects.filter(categoryID=pk)
        except Merchandise.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        merchandises = self.get_object(pk)
        serializer = MerchandiseListShowInfoSerializer(merchandises, many=True)
        for product in serializer.data:
            product['picture'] = 'https://www.wuzhuanggui.shop/media/'+product.get['code']+'.png'
        return Response(serializer.data)


class QueryMerchandiseDetailByBarcodeView(APIView):
    def post(self, request):
        serializer = QueryMerchandiseDetailByBarcodeRequestSerializer(data=request.data)
        if serializer.is_valid():
            barcode = serializer.validated_data['barcode']
            merchandise = Merchandise.objects.get(barcode=barcode)
            output_serializer = QueryMerchandiseDetailByBarcodeResponseSerializer(merchandise)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateMerchandiseView(APIView):
    def post(self, request):
        serializer = AddMerchandiseDetailByBarcodeSerializer(data=request.data)
        if serializer.is_valid():
            merchandise = serializer.create(serializer.validated_data)
            merchandise.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)