from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('chat-list/', views.chat_list, name='chat_list'),
    path('chat/<int:seller_id>/', views.chat_detail, name='chat_detail'),  # ✅ added
    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),  # ✅ add this
    # transactions/urls.py
path('chat/<int:seller_id>/delete/', views.delete_chat, name='delete_chat'),

]
