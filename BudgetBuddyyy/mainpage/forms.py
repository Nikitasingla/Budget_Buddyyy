from django import forms
from .models import Income, Expense, ExpenseLimit

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'source']
        widgets = {
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category','description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        

class LimitForm(forms.ModelForm):
    class Meta:
        model = ExpenseLimit
        fields = ['category', 'limit']



from django import forms
from .models import SharedBudget, Contribution

class SharedBudgetForm(forms.ModelForm):
    class Meta:
        model = SharedBudget
        fields = ['name', 'total_budget', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple()
        }

class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['amount', 'note']
