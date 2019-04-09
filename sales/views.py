from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# Imports from your apps
from .models import SaleRecord
from .functions import CountOrderIntoSaleRecord, RemoveOrderItemsFromStock
from .serializers import SaleRecordSerializer
from orders.serializers import OrderTradeNoSerializer

# for test only
class CountOrderIntoSaleByTradeNoView(APIView):
    def post(self, request):
        trade_no = request.data.get("tradeNo")
        result = CountOrderIntoSaleRecord(trade_no=trade_no)
        if result:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


# for test only
class RemoveOrderItemsFromStockView(APIView):
    def post(self, request):
        trade_no = request.data.get("tradeNo")
        result = RemoveOrderItemsFromStock(trade_no=trade_no)
        if result:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class SaleQueryByShopView(APIView):
    def get_object(self, pk):
        try:
            return SaleRecord.objects.filter(shop=pk).order_by('-number')
        except SaleRecord.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        sale_records = self.get_object(pk)
        serializer = SaleRecordSerializer(sale_records, many=True)
        return Response(serializer.data)


class SaleQueryByMerchandiseView(APIView):
    def get_object(self, pk):
        try:
            return SaleRecord.objects.filter(merchandise=pk).order_by('-number')
        except SaleRecord.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        sale_records = self.get_object(pk)
        serializer = SaleRecordSerializer(sale_records, many=True)
        return Response(serializer.data)
