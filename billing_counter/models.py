from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Store(models.Model):
    store_name = models.CharField(max_length=200)

    def __str__(self):
        return self.store_name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_at = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " works at " + str(self.employee_at)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_description = models.TextField()
    category = models.ForeignKey(Store, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_id = models.ForeignKey('Invoice', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.customer.user.username + " order for " + self.product.product_name


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(Order)

    def total_amount(self):
        # Calculate total amount based on the associated order items
        total = sum(order.total_amount for order in self.order_items.all())
        return total

    def __str__(self):
        return f"Invoice for {self.customer.user.username} - Total: {self.total_amount()}"
