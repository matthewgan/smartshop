from rest_framework.viewsets import ModelViewSet
from .models import Supplier
from .serializers import SupplierSerializer
from rest_framework.pagination import PageNumberPagination


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    pagination_class = None
