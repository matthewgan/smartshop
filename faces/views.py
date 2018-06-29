# Stdlib imports
import base64
import os
# from pathlib import Path
# Core Django imports
# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Imports from your apps
from SmartShop.settings import MEDIA_ROOT
from .serializers import UploadedFaceSerializer, SearchFaceUploadSerializer
from baidu.methods import register_face, create_aip_client, detect_face, search_face
from customers.models import Customer
from customers.serializers import EntranceGetInfoResponseSerializer


class RegisterFaceView(APIView):
    """
    Register user face info for the first time login the miniApp
    miniApp-face.js

    Parameters:
        uuid = user uuid
        imgFile = user face file

    Returns:
      detectRes-
      if failed, tell miniApp the reason
      if success, the register success

    Raises:
    """
    def post(self, request):
        serializer = UploadedFaceSerializer(data=request.data)
        # print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            # output_serializer = UploadedFaceSerializer(uploadedface)
            imageUrl = serializer.data.get('image')
            # imageRoot = Path(BASE_DIR+imageUrl)

            # encode img to base64
            # file = open(imageRoot, 'rb')
            name = os.path.basename(imageUrl)
            filepath = os.path.join(MEDIA_ROOT, name)
            # print(filepath)
            file = open(filepath, 'rb')
            img64 = base64.b64encode(file.read()).decode('UTF-8')

            # connect to baidu face api
            client = create_aip_client()
            detect_res = detect_face(img64, 'BASE64', client)

            # detect success -> register face
            if detect_res == 200:
                group_id = 'customer'
                userid = serializer.data.get('uuid')
                register_res = register_face(img64, 'BASE64', userid, group_id, client)
                # return Response(detect_res, status=status.HTTP_200_OK)
                return Response(register_res, status=status.HTTP_200_OK)

        else:
            return Response(400, status=status.HTTP_400_BAD_REQUEST)


class SearchUserFaceView(APIView):
    def post(self, request):
        serializer = SearchFaceUploadSerializer(data=request.data)
        if serializer.is_valid():
            upload_face = serializer.save()
            output_serializer = SearchFaceUploadSerializer(upload_face)
            imageUrl = output_serializer.data.get('image')
            # imageRoot = Path(BASE_DIR+imageUrl)

            # encode img to base64
            # file = open(imageRoot, 'rb')
            name = os.path.basename(imageUrl)
            filepath = os.path.join(MEDIA_ROOT, name)
            print(filepath)
            file = open(filepath, 'rb')
            img64 = base64.b64encode(file.read()).decode('UTF-8')

            # connect to baidu face api
            client = create_aip_client()
            detect_res = detect_face(img64, 'BASE64', client)
            if detect_res == 200:
                search_res = search_face(img64, 'BASE64', client)
                if search_res.get('status') == 200:
                    wuser = Customer.objects.get(pk=search_res.get('userid'))
                    output_serializer = EntranceGetInfoResponseSerializer(wuser)
                    return Response(output_serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


