from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.title, name='title'),
    path('search', views.search, name='search'),
    path('create', views.create, name="create"),
    path('wiki/<str:title>/edit', views.edit, name='edit'),
    path('testing', views.testing, name='testing'),
    path('random', views.random, name='random')
]
