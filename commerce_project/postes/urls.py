from django.urls import path
from . import views

app_name = "postes"
urlpatterns = [
    path('', views.index, name='index'),
    path('liker/<int:id>', views.liker, name='liker'),
    path('posteForm',views.post,name='post'),
]
