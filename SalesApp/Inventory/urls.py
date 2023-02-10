from django.urls import path
from . import views

urlpatterns=[
path('home',views.home,name='home'),
path('Products',views.Products, name='Products'),
path('',views.home, name='home'),
path('Signup',views.Signup, name='Signup'),
path('Login', views.Login, name='Login'),
path('User', views.Users, name='User'),
path('logout', views.logout, name='logout'),
path('order/<int:pk>/', views.Order, name='order'),
path('view/<int:pk>/', views.Info, name='view'),
path('edit/<int:pk>/', views.Edit, name='edit'),
path('UnfinishedTransactions', views.EditTrans, name='UnfTrans'),
path('editorder/<int:pk>/', views.ChangeTrans, name='editorder'),
path('confirmorder/<int:pk>/', views.ConfirmTrans, name='confirmorder'),
path('UserAdded', views.AddOrder, name='OrderAdded'),
path('Developer', views.Developer, name='Developer')

]