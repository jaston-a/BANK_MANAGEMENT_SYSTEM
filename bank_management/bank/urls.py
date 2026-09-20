from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, CustomLoginView,
    BranchViewSet, CustomerViewSet, AccountTypeViewSet,
    AccountViewSet, BeneficiaryViewSet, TransactionViewSet,
    AccountLookupView, StaffRegisterView,
    StaffListView, HQVaultView, FundAllocationViewSet, FinancialSummaryView,
    BranchVaultView
)

router = DefaultRouter()
router.register('branches', BranchViewSet, basename='branch')
router.register('customers', CustomerViewSet, basename='customer')
router.register('account-types', AccountTypeViewSet, basename='accounttype')
router.register('accounts', AccountViewSet, basename='account')
router.register('beneficiaries', BeneficiaryViewSet, basename='beneficiary')
router.register('transactions', TransactionViewSet, basename='transaction')
router.register('fund-allocations', FundAllocationViewSet, basename='fundallocation')

urlpatterns = [
    path('accounts/lookup/', AccountLookupView.as_view(), name='account-lookup'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/register-staff/', StaffRegisterView.as_view(), name='register-staff'),
    path('auth/staff-list/', StaffListView.as_view(), name='staff-list'),
    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('hq-vault/', HQVaultView.as_view(), name='hq-vault'),
    path('branch-vault/', BranchVaultView.as_view(), name='branch-vault'),
    path('financial-summary/', FinancialSummaryView.as_view(), name='financial-summary'),
    path('', include(router.urls)),
]