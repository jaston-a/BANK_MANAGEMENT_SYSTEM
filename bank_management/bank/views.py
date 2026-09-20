import uuid
from decimal import Decimal, InvalidOperation
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q, Sum, ProtectedError
from django.db.models.functions import TruncMonth
from rest_framework import viewsets, generics, permissions, filters, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from.models import Branch, Customer, AccountType, Account, Beneficiary, Transaction, User, HQVault, FundAllocation
from.permission import IsAdminRole
from.serializers import (
    RegisterSerializer, CustomTokenObtainPairSerializer,
    BranchSerializer, CustomerSerializer, AccountTypeSerializer,
    AccountSerializer, BeneficiarySerializer, TransactionSerializer,
    StaffRegisterSerializer,
    StaffListSerializer, StaffStatusSerializer,
    HQVaultSerializer, FundAllocationSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class StaffRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StaffRegisterSerializer
    permission_classes = [IsAdminRole]

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'branch_code']
    search_fields = ['name', 'branch_code', 'address']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminRole()]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer_id']
    search_fields = ['customer_id', 'user__username', 'user__email']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Customer.objects.none()
        if user.role == 'customer':
            return Customer.objects.filter(user=user)
        if user.role == 'staff':
            if not user.branch:
                return Customer.objects.none()
            return Customer.objects.filter(
                Q(accounts__branch=user.branch) | Q(accounts__isnull=True)
            ).distinct()
        return Customer.objects.all()

    def perform_update(self, serializer):
        user = self.request.user
        customer = serializer.instance
        if user.role == 'admin':
            serializer.save()
            return
        if user.role == 'staff':
            if not user.branch:
                raise serializers.ValidationError("You have no branch assigned.")
            has_access = customer.accounts.filter(branch=user.branch).exists() or not customer.accounts.exists()
            if not has_access:
                raise serializers.ValidationError("You can only edit customers who have an account in your branch or new customers without an account.")
            serializer.save()
            return
        raise serializers.ValidationError("You cannot edit your own profile. Please contact your branch staff or admin.")

class AccountTypeViewSet(viewsets.ModelViewSet):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminRole()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'detail': f'Cannot delete "{instance.name}" because one or more accounts are still using this account type.'},
                status=400
            )

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'account_type': ['exact'],
        'branch': ['exact'],
        'balance': ['gte', 'lte', 'exact'],
        'customer': ['exact'],
    }
    search_fields = ['account_number', 'customer__user__username']
    ordering_fields = ['balance', 'created_at']

    def get_queryset(self):
        queryset = Account.objects.all()
        user = self.request.user
        if not user.is_authenticated:
            return Account.objects.none()
        my_accounts = self.request.query_params.get('my_accounts')
        if user.role == 'customer' or my_accounts == 'true':
            try:
                customer = Customer.objects.get(user=user)
                return queryset.filter(customer=customer)
            except Customer.DoesNotExist:
                return queryset.none()
        if user.role == 'staff':
            if user.branch:
                return queryset.filter(branch=user.branch)
            return queryset.none()
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'customer':
            customer = Customer.objects.get(user=user)
            if serializer.validated_data.get('customer')!= customer:
                raise serializers.ValidationError("You can only create accounts for yourself.")
        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        if user.role not in ('admin', 'staff'):
            raise serializers.ValidationError("You do not have permission to update this account.")

        instance = serializer.instance
        new_status = serializer.validated_data.get('status')
        if new_status == 'active' and instance.status != 'active':
            customer = instance.customer
            if not customer.date_of_birth or not customer.address or not customer.aadhar_number:
                raise serializers.ValidationError(
                    "Complete KYC details required before activation. Please update the customer's date of birth, address, and Aadhar number first."
                )

        serializer.save()

class AccountLookupView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        account_number = request.query_params.get('account_number', '').strip()
        if not account_number:
            return Response({'detail': 'account_number is required'}, status=400)
        try:
            account = Account.objects.select_related('customer__user', 'branch').get(account_number=account_number)
        except Account.DoesNotExist:
            return Response({'detail': 'No account found with that number'}, status=404)
        return Response({
            'id': account.id,
            'account_number': account.account_number,
            'customer_name': account.customer.user.username,
            'branch_name': account.branch.name,
            'status': account.status,
        })

class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active', 'customer']
    search_fields = ['nickname', 'beneficiary_account__account_number']
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Beneficiary.objects.none()
        if user.role == 'customer':
            try:
                customer = Customer.objects.get(user=user)
                return Beneficiary.objects.filter(customer=customer)
            except Customer.DoesNotExist:
                return Beneficiary.objects.none()
        return Beneficiary.objects.all()
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'customer':
            customer = Customer.objects.get(user=user)
            if serializer.validated_data.get('customer')!= customer:
                raise serializers.ValidationError("You can only add beneficiaries to your own profile.")
        serializer.save()

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    http_method_names = ['get', 'post', 'head', 'options']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'status', 'account']
    search_fields = ['reference', 'description']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Transaction.objects.none()
        if user.role == 'customer':
            try:
                customer = Customer.objects.get(user=user)
            except Customer.DoesNotExist:
                return Transaction.objects.none()
            return Transaction.objects.filter(
                Q(account__customer=customer) | Q(related_account__customer=customer)
            ).distinct()
        if user.role == 'staff':
            if user.branch:
                return Transaction.objects.filter(account__branch=user.branch)
            return Transaction.objects.none()
        return Transaction.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == 'admin':
            raise serializers.ValidationError("Admins cannot perform transactions. Please use branch staff to process deposits, withdrawals, and transfers.")

        account = serializer.validated_data['account']
        amount = serializer.validated_data['amount']
        ttype = serializer.validated_data['transaction_type']
        related_account = serializer.validated_data.get('related_account')

        if user.role == 'customer':
            try:
                customer = Customer.objects.get(user=user)
            except Customer.DoesNotExist:
                raise serializers.ValidationError("Customer profile not found for this user.")
            if account.customer_id!= customer.id:
                raise serializers.ValidationError("You can only transact on your own account.")
            if ttype!= 'transfer':
                raise serializers.ValidationError("Deposits and withdrawals involve physical cash and must be done at your branch counter. You can only transfer funds online.")
            confirm_password = self.request.data.get('confirm_password')
            if not confirm_password or not user.check_password(confirm_password):
                raise serializers.ValidationError({'confirm_password': 'Incorrect password. Please confirm your password to proceed with the transfer.'})

        if user.role == 'staff' and not user.branch:
            raise serializers.ValidationError("You have no branch assigned. Please contact admin before processing transactions.")

        if account.status!= 'active':
            raise serializers.ValidationError("This account is not active yet. Please contact your branch to activate it before transacting.")
        if ttype == 'transfer' and related_account and related_account.status!= 'active':
            raise serializers.ValidationError("The destination account is not active yet. This transfer cannot be completed.")
        if related_account and account.id == related_account.id:
            raise serializers.ValidationError("Source and destination accounts cannot be the same.")
        if ttype in ('withdrawal', 'transfer') and amount > account.balance:
            raise serializers.ValidationError("Insufficient balance.")

        if ttype in ('withdrawal', 'transfer'):
            min_balance = account.account_type.minimum_balance
            if (account.balance - amount) < min_balance:
                raise serializers.ValidationError(
                    f"This transaction would drop the balance below the minimum required balance of ₹{min_balance} for this account type."
                )

        if ttype == 'deposit':
            branch = user.branch if user.role == 'staff' else account.branch
            if amount > branch.vault_balance:
                raise serializers.ValidationError(
                    f"Insufficient vault balance at {branch.name}. Only ₹{branch.vault_balance} available. Please contact HQ/Admin to allocate more funds before depositing."
                )
            account.balance += amount
            branch.vault_balance -= amount
            branch.save()
        elif ttype == 'withdrawal':
            branch = user.branch if user.role == 'staff' else account.branch
            account.balance -= amount
            branch.vault_balance += amount
            branch.save()
        elif ttype == 'transfer':
            if not related_account:
                raise serializers.ValidationError("related_account is required for transfers.")
            account.balance -= amount
            related_account.balance += amount
            related_account.save()
        account.save()
        serializer.save(
            reference=uuid.uuid4().hex[:12].upper(),
            balance_after=account.balance,
            status='completed'
        )

class StaffListView(generics.ListAPIView):
    queryset = User.objects.filter(role='staff')
    serializer_class = StaffListSerializer
    permission_classes = [IsAdminRole]

class StaffStatusView(generics.UpdateAPIView):
    queryset = User.objects.filter(role='staff')
    serializer_class = StaffStatusSerializer
    permission_classes = [IsAdminRole]

class HQVaultView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        vault = HQVault.get_instance()
        return Response(HQVaultSerializer(vault).data)

    def post(self, request):
        vault = HQVault.get_instance()
        raw_amount = request.data.get('amount')
        if raw_amount is None:
            return Response({'detail': 'amount is required'}, status=400)
        try:
            amount = Decimal(str(raw_amount))
        except (InvalidOperation, ValueError):
            return Response({'detail': 'Invalid amount'}, status=400)
        if amount <= 0:
            return Response({'detail': 'Amount must be greater than zero'}, status=400)
        vault.total_balance += amount
        vault.save()
        return Response(HQVaultSerializer(vault).data)

class FundAllocationViewSet(viewsets.ModelViewSet):
    queryset = FundAllocation.objects.all().order_by('-created_at')
    serializer_class = FundAllocationSerializer
    permission_classes = [IsAdminRole]
    http_method_names = ['get', 'post', 'head', 'options']

    def perform_create(self, serializer):
        branch = serializer.validated_data['branch']
        amount = serializer.validated_data['amount']
        vault = HQVault.get_instance()
        if amount > vault.total_balance:
            raise serializers.ValidationError("Insufficient HQ vault balance. Please add capital first.")
        vault.total_balance -= amount
        vault.save()
        branch.vault_balance += amount
        branch.save()
        serializer.save(
            allocated_by=self.request.user,
            reference=uuid.uuid4().hex[:12].upper()
        )

class BranchVaultView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'staff' or not user.branch:
            return Response({'detail': 'This view is only available for staff with an assigned branch.'}, status=403)
        return Response({
            'branch_name': user.branch.name,
            'vault_balance': float(user.branch.vault_balance),
        })

class FinancialSummaryView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        branches = Branch.objects.all()
        branch_data = []
        for b in branches:
            total_balance = Account.objects.filter(branch=b).aggregate(total=Sum('balance'))['total'] or 0
            branch_data.append({
                'branch_name': b.name,
                'vault_balance': float(b.vault_balance),
                'account_balance': float(total_balance),
            })

        hq_vault = HQVault.get_instance()

        deposits_total = Transaction.objects.filter(transaction_type='deposit').aggregate(total=Sum('amount'))['total'] or 0
        withdrawals_total = Transaction.objects.filter(transaction_type='withdrawal').aggregate(total=Sum('amount'))['total'] or 0
        transfers_total = Transaction.objects.filter(transaction_type='transfer').aggregate(total=Sum('amount'))['total'] or 0

        six_months_ago = timezone.now() - timedelta(days=180)
        monthly_qs = (
            Transaction.objects.filter(created_at__gte=six_months_ago, transaction_type__in=['deposit', 'withdrawal'])
            .annotate(month=TruncMonth('created_at'))
            .values('month', 'transaction_type')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )
        monthly_map = {}
        for row in monthly_qs:
            month_label = row['month'].strftime('%b %Y')
            if month_label not in monthly_map:
                monthly_map[month_label] = {'month': month_label, 'deposits': 0, 'withdrawals': 0}
            if row['transaction_type'] == 'deposit':
                monthly_map[month_label]['deposits'] = float(row['total'])
            else:
                monthly_map[month_label]['withdrawals'] = float(row['total'])
        monthly_trend = list(monthly_map.values())

        return Response({
            'hq_vault_balance': float(hq_vault.total_balance),
            'branch_data': branch_data,
            'deposits_total': float(deposits_total),
            'withdrawals_total': float(withdrawals_total),
            'transfers_total': float(transfers_total),
            'monthly_trend': monthly_trend,
        })