# Stdlib imports
import base64
# Core Django imports
# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Imports from your apps
from SmartShop.settings.base import BASE_DIR
from .serializers import UploadedFaceSerializer, SearchFaceUploadSerializer
from baidu.methods import registerface, createapiface, detectface, searchface
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
        print(serializer.initial_data)
        if serializer.is_valid():
            uploadedface = serializer.save()
        output_serializer = UploadedFaceSerializer(uploadedface)
        imageUrl = output_serializer.data.get('image')
        imageRoot = BASE_DIR+imageUrl

        # encode img to base64
        file = open(imageRoot, 'rb')
        img64 = base64.b64encode(file.read())

        # connect to baidu face api
        client = createapiface()
        detectRes = detectface(img64, 'BASE64', client)

        # detect success -> rigister face
        if detectRes == 200:
           groupid = 'customer'
           userid = output_serializer.data.get('uuid')
           registerres = registerface(img64, 'BASE64', userid, groupid, client)
        return Response(detectRes, status=status.HTTP_200_OK)


class SearchUserFaceView(APIView):
    def post(self, request):
        serializer = SearchFaceUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploadface = serializer.save()
            output_serializer = SearchFaceUploadSerializer(uploadface)
            imgUrl = output_serializer.data.get('image')
            # TODO
            imgRoot = MEDIA_ROOT + imgUrl[6:]

            # encode img to base64
            print(imgRoot)
            file = open(imgRoot, 'rb')
            img64 = base64.b64encode(file.read())

            # connect to baidu face api
            client = createapiface()
            detectRes = detectface(img64, 'BASE64', client)
            if detectRes == 200:
                searchres = searchface(img64, 'BASE64', client)
                if searchres.get('status') == 200:
                    wuser = Customer.objects.get(id=searchres.get('userid'))
                    output_serializer = EntranceGetInfoResponseSerializer(wuser)
                    return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


