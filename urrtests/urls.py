from django.contrib import admin
from django.urls import path, re_path

from urrtests.views import test_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('unnamed/<a>/<b>/', test_view),
    path('test1/<a>/<b>/<int:c>/', test_view, name='test1'),
    re_path(r'test2/(?P<a>.+?)/(?P<b>.+?)/(?P<c>\d+?)/', test_view, name='test2'),
]
