from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# from .models import Expense, Income, Limit

# Create your views here.
def home(request):
    return render(request,'base.html')

def register_view(request):
    if request.method=="POST":
        name=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if not name:
            messages.error(request,"Please enter Username")
        elif User.objects.filter(username=name).exists():
            messages.error(request,"User already exists")
        else:
            User.objects.create_user(username=name,password=password,email=email)
            messages.success(request,"User registered Successfully")
            return redirect('login')
    return render(request,'signup.html')
        
def login_view(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
            if user:
                login(request, user)
                messages.success(request, "User logged in successfully")
                return redirect('base')
            else:
                messages.error(request, "Invalid credentials")
        except User.DoesNotExist:
            messages.error(request, "No user found with this email")
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    messages.success(request,"User logged out successfully")
    return redirect('base')

def aboutus(request):
    return render(request,'aboutus.html')
 
from django.shortcuts import render, redirect
from .models import Income, Expense, ExpenseLimit
from django.contrib import messages
from .forms import IncomeForm, ExpenseForm, LimitForm
from django.contrib.auth.decorators import login_required

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('add_income')
    else:
        form = IncomeForm()

    incomes = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'add_income.html', {'form': form, 'incomes': incomes})

@login_required
def update_income(request, id):
    income = get_object_or_404(Income, id=id, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('add_income')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'update_income.html', {'form': form})


@login_required
def delete_income(request, id):
    income = get_object_or_404(Income, id=id, user=request.user)
    if request.method == 'POST':
        income.delete()
        return redirect('add_income')
    return render(request, 'delete_income.html', {'income': income})

# @login_required
# def add_expense(request):
#     expenses = Expense.objects.filter(user=request.user).order_by('-date')
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             expense = form.save(commit=False)
#             expense.user = request.user
#             # expense.date = timezone.now().date()
#             expense.save()
#             messages.success(request, "Expense added successfully!")
#             return redirect('add_expense')
#     else:
#         form = ExpenseForm()
#     return render(request, 'add_expense.html', {'form': form, 'expenses': expenses})

@login_required
def add_expense(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user

            # Check total spent in this category
            category = expense.category
            total_spent = Expense.objects.filter(user=request.user, category=category).aggregate(Sum('amount'))['amount__sum'] or 0
            projected_total = total_spent + expense.amount

            # Check if limit exists
            try:
                limit_obj = ExpenseLimit.objects.get(user=request.user, category=category)
                if projected_total > limit_obj.limit:
                    messages.warning(request, f"⚠️ Overspending alert! You've exceeded the ₹{limit_obj.limit} limit for {category}. Total: ₹{projected_total}")
            except ExpenseLimit.DoesNotExist:
                pass  # no limit set for this category

            expense.save()
            messages.success(request, "Expense added successfully!")
            return redirect('add_expense')
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form, 'expenses': expenses})


@login_required
def update_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            updated_expense = form.save(commit=False)
            updated_expense.user = request.user  # Set the user again
            updated_expense.save()
            return redirect('add_expense')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'update_expense.html', {'form': form})
@login_required
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    messages.success(request, "Expense deleted.")
    return redirect('add_expense')

from django.db.models import Sum

@login_required
def set_limit(request):
    form = LimitForm(request.POST or None)

    if form.is_valid():
        limit = form.save(commit=False)
        limit.user = request.user

        # Check if limit already exists for category
        existing = ExpenseLimit.objects.filter(user=request.user, category=limit.category).first()
        if existing:
            existing.limit = limit.limit
            existing.save()
        else:
            limit.save()

        messages.success(request, f"Limit set for {limit.category}!")
        return redirect('set_limit')

    # Get limits and compare with total expenses per category
    limits = ExpenseLimit.objects.filter(user=request.user)
    overspent_categories = []

    for limit in limits:
        total_spent = Expense.objects.filter(user=request.user, category=limit.category).aggregate(Sum('amount'))['amount__sum'] or 0
        if total_spent > limit.limit:
            overspent_categories.append((limit.category, total_spent, limit.limit))

    if overspent_categories:
        for category, total, limit_value in overspent_categories:
            messages.warning(request, f"Overspent in {category}! Limit: ₹{limit_value}, Spent: ₹{total}")

    return render(request, 'set_limit.html', {'form': form, 'limits': limits})


def dashboard(request):
    user = request.user
    total_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

    total_income = float(total_income)
    total_expenses = float(total_expenses)
    total_balance=total_income-total_expenses
    if total_balance < 0:
        messages.error(request, "Total Balance is negative")

    # Overspending Calculation
    overspending_total = 0
    for limit in ExpenseLimit.objects.filter(user=user):
        spent = Expense.objects.filter(user=user, category=limit.category).aggregate(Sum('amount'))['amount__sum'] or 0
        if spent > limit.limit:
            overspending_total += (spent - limit.limit)

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'overspending_total': overspending_total,
        'total_balance':total_balance
    }
    return render(request, 'dashboard.html', context)

def profile(request):
    user = request.user
    total_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

    overspending_total = 0
    for limit in ExpenseLimit.objects.filter(user=user):
        spent = Expense.objects.filter(user=user, category=limit.category).aggregate(Sum('amount'))['amount__sum'] or 0
        if spent > limit.limit:
            overspending_total += (spent - limit.limit)

    total_income = float(total_income)
    total_expenses = float(total_expenses)
    total_balance=total_income-total_expenses
    if total_balance < 0:
        messages.error(request, "Total Balance is negative")
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'overspending_total': overspending_total,
        'total_balance':total_balance
    }
    return render(request, 'profile.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from .models import SharedBudget, Contribution
from .forms import SharedBudgetForm, ContributionForm
from django.contrib.auth.decorators import login_required

@login_required
def shared_budget_list(request):
    budgets = SharedBudget.objects.filter(members=request.user)
    return render(request, 'shared_budget_list.html', {'budgets': budgets})

@login_required
def create_shared_budget(request):
    if request.method == 'POST':
        form = SharedBudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.created_by = request.user
            budget.save()
            form.save_m2m()
            return redirect('shared_budget_list')
    else:
        form = SharedBudgetForm()
    return render(request, 'create_shared_budget.html', {'form': form})


import json
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import SharedBudget, Contribution
from .forms import ContributionForm
from django.contrib.auth.decorators import login_required

@login_required
def shared_budget_detail(request, pk):
    budget = get_object_or_404(SharedBudget, pk=pk)

    if request.user not in budget.members.all():
        return redirect('shared_budget_list')

    contributions = budget.contributions.all()
    contribution_summary = contributions.values('user__username').annotate(total=Sum('amount'))

    labels = [entry['user__username'] for entry in contribution_summary]
    data = [float(entry['total']) for entry in contribution_summary]

    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.budget = budget
            contribution.user = request.user
            contribution.save()
            return redirect('shared_budget_detail', pk=pk)
    else:
        form = ContributionForm()

    return render(request, 'shared_budget_detail.html', {
        'budget': budget,
        'contributions': contributions,
        'form': form,
        'labels_json': json.dumps(labels),
        'data_json': json.dumps(data),
    })



