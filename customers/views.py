# Stdlib imports

# Core Django imports
from django.shortcuts import get_object_or_404

# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
import requests

# Imports from your apps
from .models import Customer
from .serializers import SignupRequestSerializer, SignupResponseSerializer
from .serializers import LoginRequestSerializer, LoginResponseSerializer
from .serializers import CustomerListSerializer
from .serializers import CustomerDetailSerializer, CustomerDetailGetInfoSerializer


class CustomerSignupView(APIView):
    """
        List all the wechat users, or create a new user
        miniApp-start.js

        Parameters:
          code - miniApp loginCode, save for barCode entering
          nickName -
          avatarUrl -
          gender -
          city -
          province -
          country -
          language -

        Returns:
          id - user uuid
          point -
          level -
          balance -

        Raises:
          KeyError - raises an exception
        """

    def post(self, request, *args, **kwargs):
        """
        Receive post message from wechat mini app,
        check if user is new to create a new user,
        else search the database and reply user's and infos
        """
        serializer = SignupRequestSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            # Use code to Request wxid and sessionkey from wechat API
            # appid and secret from wechat miniapp website
            secret_key = '7a3675768fa899753a775ad6e72a1816'
            app_id = 'wx18902f96ec8fb847'
            # fixed wechat API address for wx.login
            base_address = 'https://api.weixin.qq.com/sns/jscode2session?appid='
            content = base_address+app_id+'&secret='+secret_key+'&js_code='+code+'&grant_type=authorization_code'
            # request wechat API and get json response
            res = requests.get(content).json()
            if res.get('errcode') is not None:
                return Response(res, status=status.HTTP_204_NO_CONTENT)
            else:
                openid = res.get('openid')
                session_key = res.get('session_key')
                # do search on the database to see if the user is already existed
                try:
                    customer = Customer.objects.get(openid=openid)
                except Customer.DoesNotExist:
                    customer = serializer.create(serializer.validated_data)
                    customer.openid = openid
                    customer.session_key = session_key
                    customer.save()
                output_serializer = SignupResponseSerializer(customer)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerLoginView(APIView):
    """
    Set code every time user login the miniapp
    miniApp-start.js

    Parameters:
      code - miniApp loginCode, save for barCode entering
      id - user uuid

    Returns:
      id - user uuid
      point -
      level -
      balance -

    Raises:
      KeyError - raises an exception
    """
    def put(self, request):
        pk = request.data['id']
        customer = get_object_or_404(Customer, pk=pk)
        serializer = LoginRequestSerializer(customer, data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            output_serializer = LoginResponseSerializer(customer)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):
    """
    To renew user info when user into the user page
    miniApp-user.js

    Parameters:
        id - order id

    Returns:
      id - user uuid
      point -
      level -
      balance -

    Raises:
    """
    def post(self, request):
        pk = request.data['id']
        customer = get_object_or_404(Customer, pk=pk)
        output_serializer = CustomerDetailSerializer(customer)

        return Response(output_serializer.data, status=status.HTTP_200_OK)


class CustomerInfoView(APIView):
    def post(self, request):
        pk = request.data.get('id')
        customer = get_object_or_404(Customer, pk=pk)
        output_serializer = CustomerDetailGetInfoSerializer(customer)

        return Response(output_serializer.data, status=status.HTTP_200_OK)


class CustomerListView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    permission_classes = (IsAdminUser,)
