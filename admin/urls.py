from .views import *
from django.urls import path

urlpatterns = [
    path('user-details/', UserDetailsView.as_view(),name='user-details'),
    path('user-block/<int:pk>/',UserBlockView.as_view(),name='user-block'),
    path('user-unblock/<int:pk>/', UserUnBlockView.as_view(), name='user-unblock')
]
