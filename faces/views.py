# Stdlib imports
import base64
import os
import json
# from pathlib import Path
# Core Django imports
# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Imports from your apps
from SmartShop.settings import MEDIA_ROOT
from .serializers import UploadedFaceSerializer, SearchFaceUploadSerializer
from baiduaip.methods import register_face, create_aip_client, detect_face, search_face, load_image_to_base64
from customers.models import Customer
from customers.serializers import EntranceGetInfoResponseSerializer


class FaceRegisterView(APIView):
    def post(self, request):
        serializer = UploadedFaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            image = serializer.data.get('image')
            file_path = os.path.join(MEDIA_ROOT, os.path.basename(image))
            img64 = load_image_to_base64(file_path)
            if img64 == "DoesNotExist":
                return img64

            # connect to baidu face api
            client = create_aip_client()
            result = detect_face(img64, 'BASE64', client)
            error_code = result.get('error_code')
            if error_code == 0:
                face_token = result.get('face_token')
                group_id = 'customer'
                user_id = serializer.data.get('uuid')
                customer = Customer.objects.get(pk=user_id)
                result = register_face(image=face_token,
                                       image_type='FACE_TOKEN',
                                       user_id=user_id,
                                       user_info=customer.nickName,
                                       group_id=group_id,
                                       client=client)
                return Response(json.dumps(result), status=status.HTTP_200_OK)
            else:
                return Response(json.dumps(result), status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FaceSearchView(APIView):
    def post(self, request):
        serializer = SearchFaceUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            image = serializer.data.get('image')
            file_path = os.path.join(MEDIA_ROOT, os.path.basename(image))
            img64 = load_image_to_base64(file_path)
            if img64 == "DoesNotExist":
                return Response(img64, status=status.HTTP_204_NO_CONTENT)

            # connect to baidu face api
            client = create_aip_client()
            # fix id list for now
            group_id_list = 'customer'
            result = search_face(img64, 'BASE64', group_id_list, client)
            print(result)
            error_code = result.get('error_code')
            if error_code == 0:
                user_id = result.get('user_id')

                customer = Customer.objects.get(pk=user_id)
                output_serializer = EntranceGetInfoResponseSerializer(customer)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(json.dumps(result), status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
