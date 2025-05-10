
# models.py
from django.db import models
from django.contrib.auth.models import User
class Stock(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.stock.name} (x {self.quantity})"

    def get_total_price(self):
        return self.stock.price * self.quantity
    

class BoughtStocks(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    symbol=models.CharField(max_length=10)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    bought_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} at ${self.price} "


