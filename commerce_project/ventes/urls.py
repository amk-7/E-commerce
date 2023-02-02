from django.urls import path
from . import views

app_name = "ventes"
urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:id>/', views.details, name='article'),
    path('article/<int:id>/add-to-cart', views.addToCart, name="add-to-cart"),
    path('cart/', views.cart, name='cart'),
    path('article/<int:id>/note', views.note_article, name='note-article'),
    path('cart/delete/', views.delete_cart, name='delete-cart'),
]
