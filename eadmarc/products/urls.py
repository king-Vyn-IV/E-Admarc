from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('sales/', views.sales_report, name='sales_report'),
    
    path('manage/', views.manage_products, name='manage_products'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    
    path('add/', views.add_product, name='add_product'),
    path('list/', views.product_list, name='product_list'),
    
    path('submission/<int:submission_id>/approve/', views.approve_submission, name='approve_submission'),
    path('submission/<int:submission_id>/reject/', views.reject_submission, name='reject_submission'),
    
    path('market-trends/', views.market_trends_view, name='market_trends'),
    path('admin_addproduct/', views.admin_add_product, name='admin_addproduct'),
    
    path('submissions/', views.submission, name='submission'),  # <-- updated view name
    path('submissions/<int:draft_id>/delete/', views.delete_submission, name='delete_draft'),
    
    path('submissions/<int:draft_id>/edit/', views.edit_draft, name='edit_draft'),


]
