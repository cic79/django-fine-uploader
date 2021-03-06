# !/usr/bin/env python
# encoding:UTF-8

"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from myapp import views

admin.autodiscover()

urlpatterns = [
    # The Django Admin
    url(r'^admin/', admin.site.urls),

    # django-fine-uploader default urls
    url(r'^fine-uploader/', include('django_fine_uploader.urls', namespace='django_fine_uploader')),

    url(r'^$', view=views.HomeView.as_view(), name='home'),
    url(r'^custom/$', view=views.CustomView.as_view(), name='example_custom'),
    url(r'^gallery/$', view=views.GalleryView.as_view(), name='example_gallery'),
    url(r'^row/$', view=views.RowView.as_view(), name='example_row'),
    url(r'^upload/$', view=views.CustomFineUploaderView.as_view(), name='uploader'),

    # our custom views on myapp app
    url(r'^oldhome/$', view=views.ExampleView.as_view(), name='oldhome'),
    url(r'^upload-1/$', view=views.MyAppUploaderView.as_view(), name='uploader-1'),
    url(r'^upload-2/$', view=views.NotConcurrentUploaderView.as_view(), name='uploader-2'),
    url(r'^upload-3/$', view=views.SimpleCustomUploaderView.as_view(), name='uploader-3'),
    url(r'^upload-4/$', view=views.CustomFineUploaderView.as_view(), name='uploader-4'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
