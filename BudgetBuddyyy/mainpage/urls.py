from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='base'),
    path('login/',views.login_view,name='login'),
    path('signup/',views.register_view,name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('about/',views.aboutus,name='about'),
    path('add-income/', views.add_income, name='add_income'),
    path('income/update/<int:id>/', views.update_income, name='update_income'),
    path('delete-income/<int:id>/', views.delete_income, name='delete_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('update-expense/<int:id>/', views.update_expense, name='update_expense'),

    path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('set-limit/', views.set_limit, name='set_limit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/',views.profile,name='profile'),

    path('budgets/', views.shared_budget_list, name='shared_budget_list'),
    path('budgets/create/', views.create_shared_budget, name='create_shared_budget'),
    path('budgets/<int:pk>/', views.shared_budget_detail, name='shared_budget_detail'),
    
]