from django.urls import path
from . import views

urlpatterns = [
# Authentication
path('register/', views.register_view, name='register'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),

# Dashboards
path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
path('user-dashboard/', views.users_dashboard, name='users_dashboard'),
path('farmers-dashboard/', views.farmers_dashboard_view, name='farmers_dashboard'),



# Cart
path('cart/', views.cart_view, name='cart'),
# urls.py
path('cart/add/<int:submission_id>/', views.add_to_cart, name='add_to_cart'),
path('cart/update/', views.update_cart, name='update_cart'),



path('submission/<int:pk>/edit/', views.submission_edit, name='submission_edit'),
path('submission/<int:pk>/delete/', views.submission_delete, name='submission_delete'),

# User management
path('users/', views.manage_users, name='manage_users'),
path('users/add/', views.add_user, name='add_user'),
path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

]
