from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Stock, InStockRecord, OutStockRecord
from .serializers import StockSerializer, InStockRecordSerializer, OutStockRecordSerializer
from .serializers import ListStockSerializer, QueryStockSerializer
from django.db.models import Q


class CreateInStockView(APIView):
    def post(self, request):
        serializer = InStockRecordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            shop_id = serializer.validated_data['shopID']
            merchandise_id = serializer.validated_data['merchandiseID']
            in_stock_number = serializer.validated_data['number']
            # Find in Stock table and add number into total number
            stock = Stock.objects.filter(Q(shopID=shop_id) & Q(merchandiseID=merchandise_id))
            if not stock.exists():
                stock_serializer = StockSerializer(data=request.data)
                if stock_serializer.is_valid():
                    stock_serializer.save()
            else:
                stock = stock.first()
                stock.number += in_stock_number
                stock.save(force_update=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOutStockView(APIView):
    def post(self, request):
        serializer = OutStockRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            shop_id = serializer.validated_data['shopID']
            merchandise_id = serializer.validated_data['merchandiseID']
            out_stock_number = serializer.validated_data['number']
            # Find in Stock table, and sub number from total number
            stock = Stock.objects.filter(Q(shopID=shop_id) & Q(merchandiseID=merchandise_id))
            if not stock.exists():
                stock_serializer = StockSerializer(data=request.data)
                stock_serializer.validated_data['number'] = 0
                stock_serializer.save()
            else:
                stock = stock.first()
                if (stock.number - out_stock_number) > 0:
                    stock.number -= out_stock_number
                else:
                    stock.number = 0
                stock.save(force_update=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryStockView(APIView):
    def post(self, request):
        input_serializer = QueryStockSerializer(data=request.data)
        if input_serializer.is_valid():
            # Find the stock based on shop and merchandise
            shop_id = input_serializer.validated_data['shopID']
            merchandise_id = input_serializer.validated_data['merchandiseID']
            stock = Stock.objects.filter(Q(shopID=shop_id) & Q(merchandiseID=merchandise_id))
            if not stock.exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                stock = stock.first()
                output_serializer = ListStockSerializer(stock)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

