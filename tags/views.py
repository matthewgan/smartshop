# Stdlib imports
# Core Django imports
from django.http import Http404
# Third-party app imports
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
# Imports from your apps
from .models import Tag
from .serializers import TagSerializer, TagQueryResponseSerializer
from merchandises.models import Merchandise
from merchandises.serializers import MerchandiseListShowInfoSerializer
# from inventory.models import Inventory


class TagCreateView(APIView):
    """
    Create a new tag, used when do in-stock
    """
    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            # try:
            #     inventory = Inventory.objects.get(merchandiseID=serializer.data['merchandiseID'])
            #     inventory.stock = inventory.stock - 1
            #     inventory.stockWithTag = inventory.stockWithTag + 1
            #     inventory.save()
            # except:
            #
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDeleteView(DestroyAPIView):
    """
    Delete a tag from database
    """
    def get_object(self, pk):
        try:
            return Tag.objects.get(EPC=pk)
        except Tag.DoesNotExist:
            raise Http404

    def delete(self, request):
        epc = request.data.get('EPC')
        tag = self.get_object(epc)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagQueryView(APIView):
    """
    Query a list of merchandise ID by tag EPCs
    and send back the merchandises information
    NOTE : will only process on tags that already registered in the database
    """
    def post(self, request):
        taglist = request.data
        li = taglist.get('EPC')
        tags = Tag.objects.filter(EPC__in=li, status__exact=0)
        ids = tags.values_list('merchandiseID')
        merchandises = Merchandise.objects.filter(pk__in=ids)
        output_serializer = MerchandiseListShowInfoSerializer(merchandises, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class TagStatusUpdateView(APIView):
    """
    Change tags status when tags is purchased or sold
    0: just registered
    1: lock when purchased
    2: sold
    """
    def post(self, request):
        taglist = request.data
        li = taglist.get('EPC')
        tags = Tag.objects.filter(EPC__in=li)
        for tag in tags:
            tag.status = 2
            tag.save()
        output_serializer = TagSerializer(tags, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
