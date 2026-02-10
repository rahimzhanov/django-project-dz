from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls', namespace='catalog')),  # БЕЗ namespace
    path('users/', include('users.urls')),  # БЕЗ namespace
    path('blog/', include('blog.urls')),
]