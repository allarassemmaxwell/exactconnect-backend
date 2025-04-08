from rest_framework import serializers
from .models import Product, Order
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
	def validate(self, attrs):
		return attrs
	
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


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    Serializes all fields of the Product model for read/write operations.
    """
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model (read-only).

    Includes nested product data using the ProductSerializer for detailed output.
    """
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for creating orders.

    Only includes product and quantity fields. The user is set automatically in the view.
    """
    class Meta:
        model = Order
        fields = ['product', 'quantity']


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
