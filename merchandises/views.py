# Stdlib imports

# Core Django imports
from django.http import Http404

# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView

# Imports from your apps
from .models import Merchandise
from .serializers import MerchandiseListShowInfoSerializer
from .serializers import QueryMerchandiseDetailByBarcodeRequestSerializer, QueryMerchandiseDetailByBarcodeResponseSerializer
# from .serializers import MerchandiseListShowInfoForInventorySerializer
from .serializers import AddMerchandiseDetailByBarcodeSerializer, QueryMerchandiseDetailByBarcodeForCashierSerializer
from tags.models import Tag


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
        return Response(serializer.data)


class QueryMerchandiseDetailByBarcodeView(APIView):
    def post(self, request):
        serializer = QueryMerchandiseDetailByBarcodeRequestSerializer(data=request.data)
        if serializer.is_valid():
            barcode = serializer.validated_data['barcode']
            # try:
            #     merchandise = Merchandise.objects.get(barcode=barcode)
            # except Merchandise.DoesNotExist:
            #     return Response(status=status.HTTP_204_NO_CONTENT)
            # output_serializer = QueryMerchandiseDetailByBarcodeResponseSerializer(merchandise)
            # return Response(output_serializer.data, status=status.HTTP_200_OK)

            # Fix bug server 500 when there are duplicate merchandise in the database
            merchandise = Merchandise.objects.get(barcode=barcode)
            if not merchandise.exists():
                # not find the barcode in the database
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                outputs = QueryMerchandiseDetailByBarcodeResponseSerializer(merchandise, many=True)
                return Response(outputs.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryMerchandiseDetailByEPCView(APIView):
    def post(self, request):
        try:
            tag = Tag.objects.get(EPC=request.data['EPC'])
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = QueryMerchandiseDetailByBarcodeResponseSerializer(tag.merchandiseID)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateMerchandiseView(APIView):
    def post(self, request):
        print(request.data)
        serializer = AddMerchandiseDetailByBarcodeSerializer(data=request.data)
        if serializer.is_valid():
            merchandise = serializer.create(serializer.validated_data)
            merchandise.save()
            output_serializer = MerchandiseListShowInfoSerializer(merchandise)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryMerchandiseDetailByBarcodeForCashierView(APIView):
    def post(self, request):
        serializer = QueryMerchandiseDetailByBarcodeRequestSerializer(data=request.data)
        if serializer.is_valid():
            barcode = serializer.validated_data['barcode']
            merchandise = Merchandise.objects.get(barcode=barcode)
            if not merchandise.exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                output_serializer = QueryMerchandiseDetailByBarcodeForCashierSerializer(merchandise)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryMerchandiseDetailByBarcodeForInventoryView(APIView):
    def post(self, request):
        serializer = QueryMerchandiseDetailByBarcodeRequestSerializer(data=request.data)
        if serializer.is_valid():
            barcode = serializer.validated_data['barcode']
            # try:
            #     merchandise = Merchandise.objects.get(barcode=barcode)
            # except Merchandise.DoesNotExist:
            #     return Response(status=status.HTTP_204_NO_CONTENT)
            # output_serializer = MerchandiseListShowInfoForInventorySerializer(merchandise)
            # return Response(output_serializer.data, status=status.HTTP_200_OK)
            merchandise = Merchandise.objects.filter(barcode=barcode)
            if not merchandise.exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                output_serializer = MerchandiseListShowInfoSerializer(merchandise, many=True)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MerchandiseDetailView(RetrieveAPIView):
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseListShowInfoSerializer
