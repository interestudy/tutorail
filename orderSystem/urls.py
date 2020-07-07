from django.urls import path

from . import views

app_name = 'orderSystem'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('create/', views.create, name='create'),

    path('login/', views.login_view, name='login_page'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/',views.register, name='register'),
    path('modify_password', views.modify_password, name='modify_password'),

    path('viewcustomer/<str:customer_id>/', views.view_customer, name='view_customer'),
    path('updateorder/<str:order_id>/', views.update_order, name='update_order'),
    path('deleteorder/<str:order_id>/', views.delete_order, name='delete_order'),
]
