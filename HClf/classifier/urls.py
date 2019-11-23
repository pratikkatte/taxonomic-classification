from django.urls import path

from . import views

urlpatterns = [
    path('', views.predictView, name='index'),
    path('train/', views.TrainView, name="upload"),
]
