from rest_framework import generics, permissions, views
from django.http import HttpResponse
from .models import Product, Order
from .serializers import *
import csv
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import  Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView


from django.contrib.auth import get_user_model
User = get_user_model()





class UserRegisterationAPIView(GenericAPIView):
    """
    API view for user registration. Validates and creates a new user.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterationSerializer
    def post(self, request, *args, **kwargs):
        """
        Handle user registration via POST. Validates data and creates a user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user  = serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    

class LoginView(APIView):
    """
    Handles user login by validating credentials and issuing authentication tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticates user and returns tokens along with user details.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

        return Response(response_data, status=status.HTTP_200_OK)



class ProductListView(generics.ListAPIView):
    """
    API view to list products.

    - Accessible only to authenticated users.
    - Supports optional filtering by product title using query parameter (?title=).
    """
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all()
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class OrderCreateView(generics.CreateAPIView):
    """
    API view to allow authenticated users to place an order.

    Automatically assigns the currently logged-in user to the order.
    """
    serializer_class = CreateOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserOrdersView(generics.ListAPIView):
    """
    API view to list all orders placed by the authenticated user.

    Only returns orders that belong to the currently logged-in user.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class DownloadOrdersCSV(views.APIView):
    """
    API view to allow the authenticated user to download their orders as a CSV file.

    The CSV includes product name, quantity, price, and total price for each order.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        response_ = HttpResponse(content_type='text/csv')
        response_['Content-Disposition'] = 'attachment; filename="orders.csv"'

        writer = csv.writer(response_)
        writer.writerow(['Product', 'Quantity', 'Price', 'Total'])

        for order in orders:
            writer.writerow([
                order.product.title,
                order.quantity,
                order.product.price,
                order.total_price()
            ])
        return response_
