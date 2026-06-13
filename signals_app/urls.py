from django.urls import path
from . import views

urlpatterns = [
    path('sync/', views.sync_view, name='sync'),
    path('thread/', views.thread_view, name='thread'),
    path('transaction/', views.transaction_view, name='transaction'),
]
