from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('__debug__/', include('debug_toolbar.urls'))
]
