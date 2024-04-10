from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')  # To include the username of the associated User model
    password = serializers.CharField(write_only=True)  # Password will not be included when serializing

    class Meta:
        model = Employee
        fields = ['username', 'password', 'employee_at']

    def create(self, validated_data):
        # Extract the user data from validated data
        user_data = validated_data.pop('user', None)

        # Create the associated User instance
        user = User.objects.create_user(**user_data)

        # Create the Employee instance
        employee = Employee.objects.create(user=user, **validated_data)

        return employee


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')  # To include the username of the associated User model
    password = serializers.CharField(write_only=True)  # Password will not be included when serializing

    class Meta:
        model = Customer
        fields = ['username', 'password']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Store.objects.all(), slug_field='store_name')

    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(queryset=Customer.objects.all(), slug_field='user')
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='product_name')

    class Meta:
        model = Order
        fields = '__all__'





