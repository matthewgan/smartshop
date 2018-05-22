from rest_framework import  status
from rest_framework.views import APIView
from api.serializers import *
from rest_framework.response import Response
import base64
from SmartShop.settings import *
from django.http import Http404
from api.extendapi import *
from django.utils import timezone
import time
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class WUserCreateOrListView(APIView):
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

    def get(self, request, *args, **kwargs):
        """
        List all the wechat user in the database
        Need to add permission control later
        Only show to shop owners and system admins
        """
        wusers = WUser.objects.all()
        serializer = WUserListSerializer(wusers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Receive post message from wechat mini app,
        check if user is new to create a new user,
        else search the database and reply user's and infos
        """
        serializer = WUserLoginRequestSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            # Use code to Request wxid and sessionkey from wechat API
            # appid and secret from wechat miniapp website
            wxapp_secret = 'e054618417e09aa9b96b3dc472f12079'
            wxapp_appid = 'wx0c5669e2d0dca700'
            # fixed wechat API address for wx.login
            baseurl = 'https://api.weixin.qq.com/sns/jscode2session?appid='
            content = baseurl + wxapp_appid + '&secret=' + wxapp_secret + '&js_code=' + code + '&grant_type=authorization_code'
            # request wechat API and get json response
            res = requests.get(content).json()
            if res.get('errcode') is not None:
                return Response(res, status=status.HTTP_204_NO_CONTENT)
            else:
                openid = res.get('openid')
                session_key = res.get('session_key')
                # do search on the database to see if the user is already existed
                try:
                    wuser = WUser.objects.get(openid=openid)
                except WUser.DoesNotExist:
                    wuser = serializer.create(serializer.validated_data)
                    wuser.openid = openid
                    wuser.session_key = session_key
                    wuser.save()
                output_serializer = WUserLoginResponseSerializer(wuser)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WXUserSetCodeView(APIView):
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
    def put(self, request, format=None):
        pk = request.data['id']
        wuser = WUser.objects.get(pk=pk)
        serializer = WUserSetCodeRequestSerializer(wuser, data=request.data)
        if serializer.is_valid():
            wuser = serializer.save()
            output_serializer = WUserSetCodeResponseSerializer(wuser)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(APIView):
    """
    List all the categories in the database: ids & names
    miniApp-shop.js

    Parameters:

    Returns:
      all Category Info

    Raises:
    """
    def get(self, request):
        catgory = Category.objects.all()
        output_serializer = CategoryResponseSerializer(catgory, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class MerchandisesShowByCategoryView(APIView):
    """
    List all the merchandises under specified category
    miniApp-shop.js

    Parameters:

    Returns:
      all Merchandises in specified category

    Raises:
    """
    def get_object(self, pk):
        try:
            return Merchandise.objects.filter(categoryID=pk)
        except Merchandise.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        merchandises = self.get_object(pk)
        serializer = MerchandiseListShowInfoSerializer(merchandises, many=True)
        return Response(serializer.data)


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
            uploadface = serializer.save()
        output_serializer = UploadedFaceSerializer(uploadface)
        imgUrl = output_serializer.data.get('image')
        imgRoot = MEDIA_ROOT + imgUrl[6:]

        # encode img to base64
        file = open(imgRoot, 'rb')
        img64 = base64.b64encode(file.read())

        # connect to baidu face api
        client = createapiface()
        detectRes = detectface(img64, 'BASE64', client)


        # detect success -> rigister face
        if detectRes == 200:
           groupid = 'customer'
           userid = output_serializer.data.get('uuid')
           registerface(img64, 'BASE64', userid, groupid, client)

        return Response(detectRes, status=status.HTTP_200_OK)


class GetOrderNumView(APIView):
    """
    Get order number for different type(waitForPay and Inprocess)
    miniApp-user.js

    Parameters:
        id = user uuid

    Returns:
      waitNum - order status0
      processNum - order status1

    Raises:
    """
    def post(self, request):

        orderList = Order.objects.filter(userID=request.data['id'])
        waitNUm = len(orderList.filter(status=0))
        processNum = len(orderList.filter(status=1))
        res = []
        res.append(waitNUm)
        res.append(processNum)

        return Response(res, status=status.HTTP_200_OK)


class GetOrderListView(APIView):
    """
    Get order list for different type of order status
    miniApp-order.js

    Parameters:
        userID = user uuid
        status = type of order

    Returns:
      'id', 'userID', 'shopID', 'status', 'paymentMethod', 'paymentSN', 'discount', 'delivery',
      'totalPrice', 'balanceUse', 'payPrice', 'name', 'totalNum', 'comment', 'addressID', 'createTime',
      'cancelTime', 'tradeNo'
      Of select status of order

    Raises:
    """
    def post(self, request):

        orderList = Order.objects.filter(userID=request.data['userID'])
        typeList = orderList.filter(status=request.data['status'])
        serializer = OrderListShowSeralizer(typeList, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetOderDetailView(APIView):
    """
    Show the detail info of a selected order
    miniApp-detail.js

    Parameters:
        uuid = user uuid
        imgFile = user face file

    Returns:
      'id', 'userID', 'shopID', 'status', 'paymentMethod', 'paymentSN', 'discount', 'delivery', 'totalPrice',
      'balanceUse', 'payPrice', 'name', 'totalNum', 'comment', 'addressID', 'details', 'createTime', 'addName',
      'addTel', 'addDetail'

    Raises:
    """

    def post(self, request):

        order = Order.objects.get(id=request.data['id'])
        serializer = GetOrderDetailSerializer(order)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CancelOrderView(APIView):
    """
    Cancel order to change the status from 0 to 4
    miniApp-detail.js & order.js

    Parameters:
        id = order id
        userId = user id, to returen the balance bace to user_balance

    Returns:
      'ok' - cancel success

    Raises:
    """
    def post(self, request):

        order = Order.objects.get(id=request.data['id'])
        wuser = WUser.objects.get(id=request.data['userId'])
        wuser.balance = order.balanceUse
        wuser.save()
        order.status = 4
        order.cancelTime = timezone.now();
        order.save()
        return Response('ok', status=status.HTTP_200_OK)


class SubmitOrderView(APIView):
    """
    Create order in model and get data from Tencent server send to miniApp for WechatPay
    miniApp-.cart/index.js

    Parameters:
        userID - user id
        shopID -
        addressID -
        orderList -

    Returns:
      payData
      -WeChatPay package(when need wechatpay)
      -success payInfo & new balance

    Raises:
    """
    def post(self, request):

        # get data from request
        userID = request.data.get('userID')
        shopID = request.data.get('shopID')
        addressID = request.data.get('addressID')
        orderList = request.data.get('orderList')

        # get userInfo from database
        wuser = WUser.objects.get(id=userID)
        userLevel = wuser.level
        userBalance = float('%.2f' % wuser.balance)
        openID = wuser.openid

        # set orderDetail list & calculate total price
        details = []
        totalNum = 0
        totalPrice = 0
        for order in orderList:
            merchandise = Merchandise.objects.get(id=order.get('id'))
            name = merchandise.name
            priceOnBill = merchandise.originPrice
            # set price for VIP customer
            # if userLevel == 1:
            #     priceOnBill = merchandise.clubPrice
            details.append({'merchandiseID': order.get('id'), 'merchandiseNum': order.get('num'), 'priceOnbill': float('%.2f' % priceOnBill)})
            totalPrice = totalPrice + order.get('num')*float('%.2f' % priceOnBill)
            totalNum = totalNum + order.get('num')

        # prepare data for wechatPay
        timestamp = str(time.time())
        tradeNo = timestamp.replace('.','0')
        if totalPrice > userBalance:
            payPrice = totalPrice-userBalance
            balanceUse = userBalance
        else:
            payPrice = 0
            balanceUse = totalPrice
        payPrice = float('%.2f' % payPrice)
        balanceUse = float('%.2f' % balanceUse)

        # prepare data for serializer to create order
        orderdata = {'userID': userID, 'shopID': shopID, 'status': 0, 'paymentMethod': 'weChatPay', 'tradeNo': tradeNo, 'discount': 0, 'delivery': 5, 'totalPrice': totalPrice, 'balanceUse': balanceUse, 'payPrice': payPrice, 'name': name, 'totalNum': totalNum, 'comment': '', 'addressID': addressID, 'details': details}

        # save to database
        serializer = CreateOrderSerializer(data=orderdata)
        if serializer.is_valid():
            serializer.save()

            # get data for wechatPay if need to pay
            if totalPrice > userBalance:
                payData = PayOrderByWechat(payPrice, tradeNo, openID)
                wuser.balance = 0
                wuser.save()
                payData['status'] = 1
            else:
                # complete pay if balance is enough to pay
                payData = {'status': 2}
                order = Order.objects.get(tradeNo=tradeNo)
                order.status = 1
                order.payTime = timezone.now()
                wuser.balance = float('%.2f' %wuser.balance) - totalPrice
                print(wuser.balance)
                order.save()
                wuser.save()
                serializer = WUserSetCodeResponseSerializer(wuser)
                payData['balance'] = serializer.data.get('balance')

        else:
            print(serializer.errors)
            return Response('Data Error', status=status.HTTP_200_OK)

        return Response(payData, status=status.HTTP_200_OK)


class GetAddressListView(APIView):
    """
    Get addresslist
    miniApp-address.js

    Parameters:
        id - user id

    Returns:
      All addressInfo in list

    Raises:
    """
    def post(self, request):

        addressList = Address.objects.filter(who=request.data.get('id'))
        serializer = AddressListSeralizer(addressList, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SetDefaultAddressView(APIView):
    """
    Set selected address to default
    miniApp-address.js

    Parameters:
        id - user id
        addId - address id

    Returns:
      'ok' - set success

    Raises:
    """
    def post(self, request):

        addList = Address.objects.filter(who=request.data.get('id'))
        for add in addList:
            if add.isDefault:
                add.isDefault = False
                add.save()

        address = Address.objects.get(id=request.data.get('addId'))
        address.isDefault = True
        address.save()

        return Response("ok", status=status.HTTP_200_OK)


class DeleteAdressView(APIView):
    """
    Delete selected address
    miniApp-address.js

    Parameters:
        addId - address id

    Returns:
      'ok' - delete success

    Raises:
    """
    def post(self, request):

        address = Address.objects.get(id=request.data.get('addId'))
        address.delete()

        return Response("ok", status=status.HTTP_200_OK)


class AddAddressView(APIView):
    """
    Add new address
    miniApp-add-address.js

    Parameters:
        who - user uuid
        name - add'name
        telephone -
        province -
        city -
        detail -

    Returns:
      'ok' - add success
      'dataerror' - request data error

    Raises:
    """
    def post(self, request):

        serializers = AddAddressSeralizer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response("ok", status=status.HTTP_200_OK)

        return Response("dataerror", status=status.HTTP_200_OK)


class TopUpView(APIView):
    """
    Topup to add user balance
    miniApp-balance.js

    Parameters:
        id - user uuid
        amountPay - need to user wechatPay to real pay
        amountAdd - extra free balance added

    Returns:
      payData - for miniApp to request a wechatPay

    Raises:
    """
    def post(self, request):

        wuser = WUser.objects.get(id=request.data.get('id'))
        openid = wuser.openid
        balance = wuser.balance
        timestamp = str(time.time())
        tradeNo = timestamp.replace('.', '0')

        data = {'userID': request.data.get('id'), 'tradeNo': tradeNo, 'amountPay': request.data.get('amountPay'), 'amountAdd': request.data.get('amountAdd')}
        serializer = CreateTopUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            payData = PayOrderByWechat(request.data.get('amountPay'), tradeNo, openid)

        return Response(payData, status=status.HTTP_200_OK)


class PaySuccessView(APIView):
    """
    When wechatPay success, request for this Api,it will renew the order and user info, also query the tencent server to ensure the payment
    miniApp-cart/index.js & balance.js & order.js & detail.js

    Parameters:
        id - user uuid
        amountPay - need to user wechatPay to real pay
        amountAdd - extra free balance added

    Returns:
      payData - for miniApp to request a wechatPay

    Raises:
    """
    def post(self, request):
        order = Order.objects.get(tradeNo=request.data.get('tradeNo'))
        wuser = WUser.objects.get(id=request.data.get('id'))
        querydata = OrderQuery(request.data.get('tradeNo'))

        if querydata.get('status') == 200:
            order.status = 1
            wuser.point = wuser.point + order.payPrice*100
            order.paymentSN = querydata.get('transaction_id')
            order.payTime = timezone.now()
            order.save()

        wuser.save()
        serializer = WUserSetCodeResponseSerializer(wuser)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TopUpSuccessView(APIView):

    def post(self, request):
        topuporder = TopUp.objects.get(tradeNo=request.data.get('tradeNo'))
        wuser = WUser.objects.get(id=request.data.get('id'))
        querydata = OrderQuery(request.data.get('tradeNo'))

        if querydata.get('status') == 200:
            topuporder.status = 1
            wuser.balance = wuser.balance + topuporder.amountPay +topuporder.amountAdd
            wuser.level = 1
            topuporder.paymentSN = querydata.get('transaction_id')
            topuporder.save()

        wuser.save()
        serializer = WUserSetCodeResponseSerializer(wuser)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PointToBalanceView(APIView):

    def post(self, request):
        wuser = WUser.objects.get(id=request.data.get('id'))
        wuser.balance = wuser.balance +request.data.get('balanceAdd')
        wuser.point = wuser.point - request.data.get('pointUse')
        wuser.save()
        serializer = WUserSetCodeResponseSerializer(wuser)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PayOrderView(APIView):
    """
    To finish payment on order page (for order that status is 0)
    miniApp-order.js & detail.js

    Parameters:
        id - order id
        userId - user id

    Returns:
            id - user uuid
      point -
      level -
      balance -

    Raises:
    """
    def post(self, request):

        # get data from request
        print(request.data.get('id'))
        order = Order.objects.get(id=request.data.get('id'))
        wuser = WUser.objects.get(id=request.data.get('userId'))
        if order.payPrice == 0:
            order.status = 1
            order.payTime = timezone.now()
            order.save()
            serializer = WUserSetCodeResponseSerializer(wuser)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            payData = PayOrderByWechat(order.payPrice, order.tradeNo, wuser.openid)
            return Response(payData, status=status.HTTP_200_OK)


class GetUserInfoView(APIView):
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

        wuser = WUser.objects.get(id=request.data.get('id'))
        serializer = WUserSetCodeResponseSerializer(wuser)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchUserFaceView(APIView):
    """
    search face api
    for entrance use
    """
    def post(self, request):
        serializer = SearchFaceUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploadface = serializer.save()
            output_serializer = SearchFaceUploadSerializer(uploadface)
            imgUrl = output_serializer.data.get('image')
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
                    wuser = WUser.objects.get(id=searchres.get('userid'))
                    output_serializer = EntranceGetInfoResponseSerializer(wuser)
                    return Response(output_serializer.data, status=status.HTTP_200_OK)

            return Response(searchres, status=status.HTTP_200_OK)


class EntranceGetUserInfoView(APIView):
    """
    get user info from server
    for entrance use
    """
    def post(self, request):
        serializer = EntranceGetInfoRequestSerializer(data=request.data)
        if serializer.is_valid():
            wuser = WUser.objects.get(code=serializer.data.get('code'))
            output_serializer = EntranceGetInfoResponseSerializer(wuser)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def isoformat(time):
        '''
        将datetime或者timedelta对象转换成ISO 8601时间标准格式字符串
        :param time: 给定datetime或者timedelta
        :return: 根据ISO 8601时间标准格式进行输出
        '''
        if isinstance(time, datetime.datetime):  # 如果输入是datetime
            return time.isoformat();
        elif isinstance(time, datetime.timedelta):  # 如果输入时timedelta，计算其代表的时分秒
            hours = time.seconds // 3600
            minutes = time.seconds % 3600 // 60
            seconds = time.seconds % 3600 % 60
            return 'P%sDT%sH%sM%sS' % (time.days, hours, minutes, seconds)  # 将字符串进行连接

# class ShopListView(APIView):
#     """
#     List all the shop informations
#     """
#     def get(self, request):
#         shops = Shop.objects.all()
#         serializer = ShopListShowInfoSerializer(shops, many=True)
#         return Response(serializer.data)
#
# class GetTencentNotifyView(APIView):
#
#     authentication_classes = (TokenAuthentication)
#     permission_classes = (IsAuthenticated,)
#     def post(self, request):
#
#         if request.data.get('return_code') == 'SUCCESS':
#             res = {'return_code':'SUCCESS','return_msg':''}
#
#             return Response(res, status=status.HTTP_200_OK)
#
# class CustomerViewSet(viewsets.ModelViewSet):
#     """
#         This viewset automatically provides `list` and `detail` actions.
#     """
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#
#     # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#     #                       IsOwnerOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class OwnerViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     This viewset automatically provides `list` and `detail` actions.
#     """
#     queryset = User.objects.all()
#     serializer_class = OwnerSerializer
#
#
# class WxUserViewSet(viewsets.ModelViewSet):
#     queryset = WxUser.objects.all()
#     serializer_class = WxUserSerializer
#     # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#
# @authentication_classes([])
# @permission_classes([])
# class ShopViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Shop.objects.all()
#     serializer_class = ShopSerializer
#
#
# class RackViewSet(viewsets.ModelViewSet):
#     queryset = Rack.objects.all()
#     serializer_class = RackSerializer
#
#
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class SupplierViewSet(viewsets.ModelViewSet):
#     queryset = Supplier.objects.all()
#     serializer_class = SupplierSerializer
#
#
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class ESLViewSet(viewsets.ModelViewSet):
#     queryset = ESL.objects.all()
#     serializer_class = ESLSerializer
#
#
# class RFIDViewSet(viewsets.ModelViewSet):
#     queryset = RFID.objects.all()
#     serializer_class = RFIDSerializer
#
#
# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer