from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", RedirectView.as_view(url='main/home/', permanent=True)),

    path('admin/', admin.site.urls),
    path('main/', include("newsportal.urls")),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
]
