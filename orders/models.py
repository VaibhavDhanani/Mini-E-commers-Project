from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.name}"

    class Meta:
        verbose_name = 'Order'
        db_table = 'orders'
        
        
class OrderItem(models.Model):
    order= models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}" 