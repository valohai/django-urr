from django.contrib import admin

from urrtests.views import test_view

try:
    from django.urls import path, re_path

    urlpatterns = [
        path("admin/", admin.site.urls),
        path("unnamed/<a>/<b>/", test_view),
        path("test1/<a>/<b>/<int:c>/", test_view, name="test1"),
        re_path(r"test2/(?P<a>.+?)/(?P<b>.+?)/(?P<c>\d+?)/", test_view, name="test2"),
        re_path(r"test3/(.+?)/(.+?)/(\d+?)/", test_view, name="test3"),
    ]
except ImportError:  # Django 1.11
    from django.conf.urls import url

    urlpatterns = [
        url("admin/", admin.site.urls),
        url("unnamed/(?P<a>.+?)/(?P<b>.+?)/", test_view),
        url("test1/(?P<a>.+?)/(?P<b>.+?)/(?P<c>[0-9]+?)/", test_view, name="test1"),
        url(r"test2/(?P<a>.+?)/(?P<b>.+?)/(?P<c>\d+?)/", test_view, name="test2"),
        url(r"test3/(.+?)/(.+?)/(\d+?)/", test_view, name="test3"),
    ]
