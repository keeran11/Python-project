
from django.urls import path
from .import views

app_name = 'payment'
urlpatterns = [
    path('', views.payment_index, name='payment_index'),
    path('CheckinListView', views.CheckinListView.as_view(), name='CheckinListView'),
    path('checkin_show/<str:check_id>', views.checkin_show, name='checkin_show'),
    path('CheckInDetailView/<str:pk>/', views.CheckInDetailView.as_view(), name='CheckInDetailView'),
    path('checkoutList/', views.checkoutList.as_view(), name='checkoutList'),
    path('checkout_show/<str:check_id>', views.checkout_show, name='checkout_show'),
    path('checkoutList/<str:pk>/', views.CheckoutDetails.as_view(), name='CheckoutDetails'),
]