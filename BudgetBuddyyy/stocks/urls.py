from django.urls import path
from stocks import views

urlpatterns=[
    path('',views.homed,name='home'),
    path('stocked/', views.stock_list, name='stock_list'),
    path('add-to-cart/<int:stock_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/delete/<int:item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('search/', views.search_stock_view, name='search_stock'),
    path('buy/',views.buy_stock,name='buy_stock'),
    path('bought/',views.bought_stocks_view,name='bought_stocks'),
    path('posted/',views.add_stock_view,name='added'),
    path('updated/<str:symbol>/',views.update_stocks,name='update'),
    path('del/<str:symbol>/',views.delete_stock,name='del')
]