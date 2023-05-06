from .views import *
from django.urls import path

urlpatterns=[
    path('add-details/', AddTurfDetailsView.as_view(),name='add-details'),
    path('get-details/', TurfDetailsView.as_view(),name='get-details'),
    path('get-details/<int:pk>/', TurfRetrieveUpdateDestroyView.as_view(), name='get_details/id'),
    path('approve-turf/<int:pk>/', ApproveTurfView.as_view(), name='approve-turf'),
    path('view-turf/<int:pk>/', ViewTurfUserView.as_view(), name='view-turf'),
    path('reject-turf/<int:pk>/', RejectTurfView.as_view(), name='approve-turf'),
    path('add-pricing/',SetTurfPriceView.as_view(), name='add-pricing'),
    path('add-review/',AddReviewRatingView.as_view(), name='add-review'),
    path('show-review/<int:pk>/',ShowReviewView.as_view(), name='show-review'),
    path('top-rated/',TopRatedView.as_view(), name='top-rated'),
    path('earnings/<int:pk>/',EarningsView.as_view(), name='earnings'),
    path('withdrawn-earnings/<int:pk>/',WithdrawnEarningsView.as_view(), name='withdrawn-earnings'),
    path('edit-turf/<int:pk>/', EditTurfView.as_view(), name='edit-turf'),
    path('unlist-turf/<int:pk>/', UnlistTurfView.as_view(), name='unlist-turf'),
    path('update-pricing/<int:pk>/', UpdateTurfPriceView.as_view(), name='update-pricing'),
]