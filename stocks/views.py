from django.db.models import Q
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Stock, InStockRecord, OutStockRecord
from .serializers import StockSerializer, InStockRecordSerializer, OutStockRecordSerializer
from .serializers import ListStockSerializer, QueryStockSerializer, TransferStockRecordSerializer
from suppliers.models import Supplier


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
                stock.instock(in_stock_number)
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
                stock.outstock(out_stock_number)
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


class TransferStockView(APIView):
    def post(self, request):
        input_serializer = TransferStockRecordSerializer(data=request.data)
        if input_serializer.is_valid():
            transfer_record = input_serializer.save()
            from_shop_id = input_serializer.validated_data["fromShop"]
            to_shop_id = input_serializer.validated_data["toShop"]
            merchandise_id = input_serializer.validated_data['merchandiseID']
            transfer_number = input_serializer.validated_data['number']
            from_shop_stock = Stock.objects.filter(Q(shopID=from_shop_id) & Q(merchandiseID=merchandise_id))
            default_supplier = Supplier.objects.all().first()
            if not from_shop_stock.exists():
                # create a empty stock for merchandise
                stock = Stock.objects.create(shopID=from_shop_id, merchandiseID=merchandise_id,
                                             number=0, supplierID=default_supplier)
                output_serializer = ListStockSerializer(stock)
                return Response(output_serializer.data, status=status.HTTP_204_NO_CONTENT)
            else:
                from_stock = from_shop_stock.first()
                if from_stock.number < transfer_number:
                    # stock number is less than request transfer number
                    output_serializer = ListStockSerializer(from_stock)
                    return Response(output_serializer.data, status=status.HTTP_204_NO_CONTENT)
                else:
                    # enough stock, can transfer to other shop
                    to_shop_stock = Stock.objects.filter(Q(shopID=to_shop_id) & Q(merchandiseID=merchandise_id))
                    if not to_shop_stock.exists():
                        # create a empty stock in to-shop for merchandise
                        to_stock = Stock.objects.create(shopID=to_shop_id, merchandiseID=merchandise_id,
                                                        number=0, supplierID=default_supplier)
                    else:
                        to_stock = to_shop_stock.first()
                    # do the transfer
                    to_stock.instock(transfer_number)
                    from_stock.outstock(transfer_number)
                    # set transfer result
                    transfer_record.result = True
                    transfer_record.save()

                    # return the new stock info of to-shop to front end
                    output_serializer = ListStockSerializer(to_stock)
                    return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryStockByShopView(APIView):
    def get_object(self, pk):
        try:
            return Stock.objects.filter(shopID=pk).order_by('-number')
        except Stock.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        stocks = self.get_object(pk)
        serializer = ListStockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QueryStockByMerchandiseView(APIView):
    def get_object(self, pk):
        try:
            return Stock.objects.filter(merchandiseID=pk).order_by('-number')
        except Stock.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        stocks = self.get_object(pk)
        serializer = ListStockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
