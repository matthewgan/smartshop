# Stdlib imports
# Core Django imports
from django.conf.urls import url
# Third-party app imports
# Imports from your apps
from .views import GetTencentNotifyView, PayOrderPreProcess, PaySuccessView, GetAlipayNotifyView, OfflinePayQueryView, \
    OfflinePayCancelView


urlpatterns = [
    url(r'^wechatnotify/$', GetTencentNotifyView.as_view()),
    url(r'^alipaynotify/$', GetAlipayNotifyView.as_view()),
    url(r'^payOrder/$', PayOrderPreProcess.as_view()),
    url(r'^paySuccess/$', PaySuccessView.as_view()),
    url(r'^offlineQuery/$', OfflinePayQueryView.as_view()),
    url(r'^offlineCancel/$', OfflinePayCancelView.as_view()),

]