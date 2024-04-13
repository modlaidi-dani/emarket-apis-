from django.urls import path
from . import views

urlpatterns = [
    path('produits', views.all_poduit, name='produits'),
    path('produit/<str:pk>', views.poduit, name='produit'),
    path('produit/creation/', views.creat_produit, name='creation'),    
    path('produit/update/<str:pk>', views.udate_produit, name='update'),
    path('produit/delete/<str:pk>', views.dlete, name='delete'),
    path('<str:pk>/review', views.review, name='createReview'),
    path('<str:pk>/review/delete', views.review_dlete, name='deleteReview'),
    
    

]