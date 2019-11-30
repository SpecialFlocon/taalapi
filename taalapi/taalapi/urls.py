from django.conf.urls import include
from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from lidwoorden import views as lidwoorden_views


api_router = DefaultRouter()
api_router.register('lidwoorden', lidwoorden_views.LidwoordenViewSet)
api_router.register('woorden', lidwoorden_views.WoordenViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_router.urls)),
]
