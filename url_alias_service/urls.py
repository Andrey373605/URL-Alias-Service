from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from short_urls.views import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('short_urls.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    re_path(r'^(?P<short_key>[a-zA-Z0-9]+)/$', RedirectView.as_view(), name='redirect'),
]