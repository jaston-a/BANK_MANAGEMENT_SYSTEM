from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('staff', 'Bank Staff'),
        ('admin', 'Admin'),
    )
    branch = models.ForeignKey('Branch', null=True, blank=True, on_delete=models.SET_NULL, related_name='staff_members')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    pan_number = models.CharField(max_length=10, blank=True)
    aadhar_number = models.CharField(max_length=12, blank=True)

class Branch(models.Model):
    name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    vault_balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.branch_code}"

class Customer(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='customer_profile'
    )
    customer_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    aadhar_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    minimum_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Account(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('blocked', 'Blocked'),
        ('closed', 'Closed'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='accounts')
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT, related_name='accounts')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_number

class Beneficiary(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='beneficiaries')
    beneficiary_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='beneficiary_records')
    nickname = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} -> {self.beneficiary_account}"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('reversed', 'Reversed'),
    )

    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    reference = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    related_account = models.ForeignKey(
        Account, 
        on_delete=models.PROTECT, 
        related_name='related_transactions', 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference

class HQVault(models.Model):
    total_balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"HQ Vault - Rs.{self.total_balance}"

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

class FundAllocation(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='fund_allocations')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    allocated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='fund_allocations_made')
    reference = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reference} - {self.branch.name} - Rs.{self.amount}"