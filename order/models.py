from django.db import models

# Parent Model
class Order(models.Model):
    order_number = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number} by {self.customer_name}"

# Child Model - ProductOrder
class ProductOrder(Order):
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Product Order {self.order_number}: {self.product_name} x {self.quantity}"

# Child Model - ServiceOrder
class ServiceOrder(Order):
    service_description = models.CharField(max_length=255)
    service_duration = models.DecimalField(max_digits=5, decimal_places=2)  # duration in hours

    def __str__(self):
        return f"Service Order {self.order_number}: {self.service_description} ({self.service_duration} hours)"
