from rest_framework.schemas import get_schema_view
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'customer', views.CustomerViewSet)
router.register(r'owner', views.OwnerViewSet)
router.register(r'wxuser', views.WxUserViewSet)
router.register(r'shop', views.ShopViewSet)
router.register(r'rack', views.RackViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'supplier', views.SupplierViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'esl', views.ESLViewSet)
router.register(r'rfid', views.RFIDViewSet)
router.register(r'order', views.OrderViewSet)


API_TITLE = 'SmartShop API'
API_DESCRIPTION = 'A Web API for creating and viewing cloud database.'
schema_view = get_schema_view(title=API_TITLE)


urlpatterns = [
    url(r'^', include(router.urls, namespace='api')),
    url(r'^test/$', TestView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^schema/$', schema_view),
    url(r'^docs/', include_docs_urls(title=API_TITLE,
                                     description=API_DESCRIPTION),
        ),
]