# from django.db import models

# Create your models here.
from django.db import models
# from django.contrib.auth.models import User

# class Expense(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
#     amount = models.FloatField()
#     category = models.CharField(max_length=50)
#     description = models.CharField(max_length=200, blank=True, null=True)
#     date = models.DateTimeField(auto_now_add=True)
#     payment_mode = models.CharField(max_length=50, blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.amount} ({self.category})"


# class Income(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income')
#     amount = models.FloatField()
#     source = models.CharField(max_length=50)
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.amount} ({self.source})"


# class Limit(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='limits')
#     category = models.CharField(max_length=50)
#     amount = models.FloatField()

#     def __str__(self):
#         return f"{self.user.username} - {self.category}: {self.amount}"
from django.db import models
from django.contrib.auth.models import User

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} - ₹{self.amount}"

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Shopping','Shopping'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
        ('Others', 'Others'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"

class ExpenseLimit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    limit = models.FloatField()

    def __str__(self):
        return f"{self.category} - {self.limit}"


from django.db import models
from django.contrib.auth.models import User

class SharedBudget(models.Model):
    name = models.CharField(max_length=100)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_shared_budgets')
    members = models.ManyToManyField(User, related_name='shared_budgets')

    def __str__(self):
        return self.name

class Contribution(models.Model):
    budget = models.ForeignKey(SharedBudget, on_delete=models.CASCADE, related_name='contributions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
