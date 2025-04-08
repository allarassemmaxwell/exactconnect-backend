from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterationAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('products/', ProductListView.as_view(), name='product_list'),
    path('orders/', OrderCreateView.as_view(), name='create_order'),
    path('my-orders/', UserOrdersView.as_view(), name='user_orders'),
]
