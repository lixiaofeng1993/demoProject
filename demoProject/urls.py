"""
URL configuration for demoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static, serve
from django.conf import settings

from demoProject import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),  # 首页
    path('login/action/', views.login, name="login"),  # 登录
    path('logout/', views.logout, name="logout"),  # 注销
    path('lock/', views.lock, name="lock"),  # 锁定屏幕
    path("modify/pwd/", views.modify_password, name="modify_pwd"),  # 修改密码
    path("forget/pwd/", views.forget_password, name="forget_pwd"),  # 忘记密码
    path("rest/pwd/", views.rest_password, name="rest_password"),  # 忘记密码
    re_path(r'static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),

    path("nb/", include("nb.urls")),

    # re_path('media/(?P<path>.*?)', serve, kwargs={'document_root': settings.MEDIA_ROOT})
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found
handler500 = views.server_error