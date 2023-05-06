from .views import *
from django.urls import path

urlpatterns = [
    path('check-availible/',CheckSlotAvailibilityView.as_view(),name='check-availible'),
    path('create-booking/',CreateBookingView.as_view(),name='create-booking'),
    path('view-bookings/',ViewBookings.as_view(),name='view-bookins'),
    # path('user'),
    path('view-booking-turf/<int:pk>/',ViewBookingForTurf.as_view(), name = 'view-booking-turf'),
    path('view-booking-user/<int:pk>/',ViewBookingForUser.as_view(), name = 'view-booking-user'),
    path('cancel-booking/<int:pk>/', CancelBookingAdmin.as_view(), name = 'cancel-booking')
]
