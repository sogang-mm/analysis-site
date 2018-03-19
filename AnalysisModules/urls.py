from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from AnalysisModules import views


router = DefaultRouter()

router.register(r'image', views.ImageViewSet)
router.register(r'module', views.ModulesViewSet)
router.register(r'result', views.ResultViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
