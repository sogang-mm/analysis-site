"""AnalysisSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
import ModuleCommunicator.views
import ModuleManager.views


router = DefaultRouter()

router.register(r'analyzer', ModuleCommunicator.views.ImageViewSet)
router.register(r'module/group', ModuleManager.views.ModuleGroupViewSet)
router.register(r'module/element', ModuleManager.views.ModuleElementViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
