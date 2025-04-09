from rest_framework import serializers
from .models import Product, Order, OrderItem
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegisterationSerializer(serializers.ModelSerializer):
	""" 
    Serializer for user registration with validation
	for password and required fields.
    """
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	class Meta:
		model  = User
		fields = ("first_name", "last_name", "email", "password")
		extra_kwargs = {"password": {"write_only": True}}
	
	def create(self, validated_data):
		return User.objects.create_user(**validated_data)
	

class LoginSerializer(serializers.Serializer):
    """
    Serializer for handling user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Custom validation method to authenticate the user.
        """
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user is None or not user.is_active:
            raise serializers.ValidationError("Invalid credentials or user is inactive")
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles user creation with username and password fields.
    """
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        """
        Creates a new user instance using the Django User model's create_user method.
        """
        user = User.objects.create_user(**validated_data)
        return user


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    Serializes all fields of the Product model for read/write operations.
    """
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.
    """
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'quantity', 'total_price']

    def validate_quantity(self, value):
        """
        Ensure that the quantity is at least 1.
        """
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an order, including order items.
    """
    orderitems = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['orderitems', 'is_active']

    def create(self, validated_data):
        """
        Create the order and the order items.
        """
        orderitems_data = validated_data.pop('orderitems')
        order = Order.objects.create(**validated_data)

        for item_data in orderitems_data:
            OrderItem.objects.create(order=order, **item_data)

        return order


class UserOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user's orders and their related order items.
    """
    orderitems = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'reference', 'orderitems', 'created_at', 'total_price']
