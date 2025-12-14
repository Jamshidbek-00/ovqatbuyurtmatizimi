from django.shortcuts import render
from rest_framework import generics, permissions
from .models import User, Food, Order
from .serializers import UserSerializer, FoodSerializer, OrderSerializer
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Create your views here.


@extend_schema(
    summary="Tizimga kirish (JWT Token olish)",
    description="Foydalanuvchi telefon raqami va paroli orqali JWT token oladi.",
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(
    summary="Token yangilash",
    description="Yangi JWT token olish uchun refresh tokenni yangilash.",
)
class CustomTokenRefreshView(TokenRefreshView):
    pass



class IsAdminUserRole(permissions.BasePermission):
    """
    Faqat admin ro'lidagi foydalanuvchilar uchun ruxsat beradi.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    


@extend_schema(
    summary="Foydalanuvchi ro'yxatdan o'tkazish",
    description="Yangi foydalanuvchi telefon raqami va paroli bilan ro'yxatdan o'tkaziladi.",
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]



class FoodPagination(PageNumberPagination):
    page_size = 10



@extend_schema(
    summary="Ovqatlar ro'yxati",
    description="""
    Barcha mavjud taomlar ro'yxatini ko'rsatadi.
    Filterlash turi bo'yicha amalga oshirilishi mumkin.
    Har bir sahifada 10 ta taom ko'rsatiladi.
    Faqat admin foydalanuvchilar yangi taom qo'shishlari mumkin.
    """
)
class FoodListView(generics.ListCreateAPIView):
    queryset = Food.objects.filter(mavjud=True)
    serializer_class = FoodSerializer
    pagination_class = FoodPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['turi']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUserRole()]
        return [permissions.AllowAny()]



@extend_schema(
    summary="Mening buyurtmalarim",
    description="""
    Avtorizatsiyadan o'tgan foydalanuvchilar o'zlarining barcha buyurtmalarini ko'rishlari mumkin.
    """
)
class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    


@extend_schema(
    summary="Yangi buyurtma yaratish",
    description="""
    Avtorizatsiyadan o'tgan foydalanuvchilar yangi buyurtma yaratishlari mumkin.
    """
)
class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context



@extend_schema(
    summary="Taomni ko'rish va tahrirlash(faqat admin uchun)",
    description="""
    Admin foydalanuvchilar taom ma'lumotlarini ko'rish, yangilash va o'chirishlari mumkin.
    """
)
class FoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAdminUserRole]
    