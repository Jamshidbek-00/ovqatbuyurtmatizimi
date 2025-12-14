from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, RegisterView, FoodListView, MyOrdersView, OrderCreateView, FoodDetailView 


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('foods/', FoodListView.as_view(), name='food_list'),
    path('my-orders/', MyOrdersView.as_view(), name='my_orders'),
    path('foods/<int:pk>/', FoodDetailView.as_view(), name='food_detail'),
    path('orders/', OrderCreateView.as_view(), name='order_create'),

]