
from . import views
from django.urls import path


urlpatterns = [
    path('', views.main, name='main'),
    path('index', views.index, name='index'),
    path('menu', views.dishes, name='menu'),
    path('type/<int:type_id>/',views.show_type,name='type'),
    path('order/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('orders/', views.order_list, name='order_list'),
    path('cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('save/', views.save_order, name='save_order'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('remove/<int:dish_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('order/<int:order_id>/report/', views.generate_report, name='order_report'),
    path('generate_report/', views.generate_report_all, name='generate_report_all'),

]

