from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
# from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .models import *
from .permissions import *


# Create your views here.

# Employee Views


class EmployeeRegisterCreateView(CreateAPIView):
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        # Serialize the request data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Create User instance
            user = User.objects.create_user(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()

            # Create Employee instance
            employee = Employee.objects.create(user=user, employee_type=request.data['employee_type'])
            employee.save()

            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeLoginCreateView(CreateAPIView):
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response("missing user", status=status.HTTP_404_NOT_FOUND)
        employee = get_object_or_404(Employee,user=user)

        token, created = Token.objects.get_or_create(user=user)
        serializer = EmployeeSerializer(employee)
        print(serializer.data)
        return Response({'token': token.key, 'user': serializer.data})

# Product Views


class ProductListView(ListAPIView):
    """
    API endpoint that allows products to be viewed
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(CreateAPIView):
    """
    API endpoint that allows products to be viewed
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsEmployee]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            employee = Employee.objects.get(user=request.user)
            if serializer.validated_data['category'] == employee.employee_at:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'Error':'You are not working in '+str(serializer.validated_data['category'])}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveView(RetrieveAPIView):
    """
    API endpoint that allows products to be viewed
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateView(UpdateAPIView):
    """
    API endpoint that allows products to be viewed
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDestroyView(DestroyAPIView):
    """
    API endpoint that allows products to be viewed
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Customer Views


class CustomerRegisterView(CreateAPIView):
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        # Serialize the request data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Create User instance
            user = User.objects.create_user(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()

            # Create Employee instance
            customer = Customer.objects.create(user=user)
            customer.save()

            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerLoginCreateView(CreateAPIView):
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response("missing user", status=status.HTTP_404_NOT_FOUND)
        employee = get_object_or_404(Customer,user=user)

        token, created = Token.objects.get_or_create(user=user)
        serializer = CustomerSerializer(employee)
        print(serializer.data)
        return Response({'token': token.key, 'user': serializer.data})


# Orders Views

class OrderCreateView(CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():

            user = get_object_or_404(User, username=request.data['customer'])
            customer = get_object_or_404(Customer,user=user)

            product = get_object_or_404(Product, product_name=request.data['product'])

            serializer.validated_data['customer'] = customer
            serializer.validated_data['product'] = product
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







