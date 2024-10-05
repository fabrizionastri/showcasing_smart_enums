from .models import ProductOrder, ServiceOrder

# Create an instance of ProductOrder
product_order = ProductOrder(
    order_number='PO123',
    customer_name='John Doe',
    product_name='Laptop',
    quantity=2
)
product_order.save()

# Create an instance of ServiceOrder
service_order = ServiceOrder(
    order_number='SO456',
    customer_name='Jane Smith',
    service_description='Website Development',
    service_duration=10.5
)
service_order.save()

# Verify instances
print(ProductOrder.objects.all())
print(ServiceOrder.objects.all()[1])

print(ProductOrder.objects.all())
print(ServiceOrder.objects.all())