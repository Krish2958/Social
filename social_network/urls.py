"""
URL configuration for social_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, FriendRequestViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.openapi import Info, License
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from .env_variables import EnvVariables

router = DefaultRouter()

# API
documentation_schema_view = get_schema_view(
    Info(
        title=" Social API",
        default_version="v1",
        description="This is the API engine for Social Web App.",
        license=License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'friend-requests', FriendRequestViewSet, basename='friend-request')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if int(EnvVariables.DEBUG.value) == 1:
    urlpatterns.append(
        path(
            "documentation/",
            documentation_schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    )