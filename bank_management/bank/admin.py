from django.contrib import admin
from .models import User, Branch, Customer, AccountType, Account, Beneficiary, Transaction, HQVault, FundAllocation

admin.site.register(User)
admin.site.register(Branch)
admin.site.register(Customer)
admin.site.register(AccountType)
admin.site.register(Account)
admin.site.register(Beneficiary)
admin.site.register(Transaction)
admin.site.register(HQVault)
admin.site.register(FundAllocation)