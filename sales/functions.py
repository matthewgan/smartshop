from django.db.models import Q
from .models import SaleRecord
from orders.models import Order, OrderDetail
from stocks.models import Stock
from suppliers.models import Supplier


def CountOrderIntoSaleRecord(trade_no):
    try:
        order = Order.objects.get(tradeNo=trade_no)
        shop = order.shopID
        if (order.status == 2) or (order.status == 3):
            # Only count when order is paid through wechat or offline
            order_details = OrderDetail.objects.filter(orderID=order.id)
            if not order_details:
                return False
            else:
                for detail in order_details:
                    merchandise = detail.merchandiseID
                    number = detail.merchandiseNum
                    sale_record = SaleRecord.objects.filter(Q(shop=shop) and Q(merchandise=merchandise))
                    if not sale_record:
                        sale_record = SaleRecord.objects.create(shop=shop, merchandise=merchandise, number=number)
                        sale_record.save()
                    else:
                        sale_record = sale_record.first()
                        sale_record.record(number)
                return True
    except:
        return False


def RemoveOrderItemsFromStock(trade_no):
    try:
        order = Order.objects.get(tradeNo=trade_no)
        shop = order.shopID
        if (order.status == 2) or (order.status == 3):
            # Only count when order is paid through wechat or offline
            order_details = OrderDetail.objects.filter(orderID=order.id)
            if not order_details:
                return False
            else:
                for detail in order_details:
                    merchandise = detail.merchandiseID
                    number = detail.merchandiseNum
                    # find stock based on shop and merchandise
                    stock = Stock.objects.filter(Q(shopID=shop) and Q(merchandiseID=merchandise))
                    if not stock.exists():
                        supplier = Supplier.objects.first()
                        stock = Stock.objects.create(shopID=shop, merchandiseID=merchandise, number=0, supplierID=supplier)
                        stock.save()
                        print(stock)
                    else:
                        stock = stock.first()
                        stock.outstock(number)
                return True
    except:
        return False
