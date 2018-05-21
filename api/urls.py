from rest_framework.schemas import get_schema_view
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from api import views
from rest_framework.authtoken import views as rest_framework_views


API_TITLE = 'SmartShop API'
API_DESCRIPTION = 'A Web API for creating and viewing cloud database.'
schema_view = get_schema_view(title=API_TITLE)


urlpatterns = [
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name="get_auth_token"),
    url(r'^wxApp/login/$', views.WUserCreateOrListView.as_view()),
    url(r'^wxApp/setCode/$', views.WXUserSetCodeView.as_view()),
    url(r'^wxApp/category/$', views.CategoryListView.as_view()),
    url(r'^wxApp/category/(?P<pk>[0-9]+)/$', views.MerchandisesShowByCategoryView.as_view()),
    url(r'^shop/$', views.ShopListView.as_view()),
    url(r'^schema/$', schema_view),
    url(r'^docs/', include_docs_urls(title=API_TITLE,
                                     description=API_DESCRIPTION),
        ),
    url(r'^wxApp/registerFace/$', views.RegisterFaceView.as_view()),
    url(r'^entry_by_code/$', views.EntranceGetUserInfoView.as_view()),
    url(r'^entry_by_face/$', views.SearchUserFaceView.as_view()),
    url(r'^wxApp/getOrder/$', views.GetOrderListView.as_view()),
    url(r'^wxApp/getOrderDetail/$', views.GetOderDetailView.as_view()),
    url(r'^wxApp/pay/$', views.PayOrderByWechatView.as_view()),
    url(r'^wxApp/submitOrder/$', views.SubmitOrderView.as_view()),
    url(r'^wxApp/getAddressList/$', views.GetAddressListView.as_view()),
    url(r'^wxApp/setDefaultAdd/$', views.SetDefaultAddressView.as_view()),
    url(r'^wxApp/deleteAddress/$', views.DeleteAdressView.as_view()),
    url(r'^wxApp/addAddress/$', views.AddAddressView.as_view()),
    url(r'^wxApp/getOrderNum/$', views.GetOrderNumView.as_view()),
    url(r'^wxApp/cancelOrder/$', views.CancelOrderView.as_view()),
    url(r'^tencent/payNotify/$', views.GetTencentNotifyView.as_view()),
    url(r'^wxApp/topUp/$', views.TopUpView.as_view()),
    url(r'^wxApp/paySuccess/$', views.PaySuccessView.as_view()),
    url(r'^wxApp/topUpSuccess/$', views.TopUpSuccessView.as_view()),
    url(r'^wxApp/pointToBalance/$', views.PointToBalanceView.as_view()),
    url(r'^wxApp/payOrder/$', views.PayOrderView.as_view()),
    url(r'^wxApp/getuserInfo/$', views.GetUserInfoView.as_view()),
]
