from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Branch, Customer, AccountType, Account, Beneficiary, Transaction, HQVault, FundAllocation

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username','email','password','password_confirm','first_name','last_name','phone','role']
        read_only_fields = ['id','role']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_phone(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if value and len(value) != 10:
            raise serializers.ValidationError("Phone number must contain 10 digits.")
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        validated_data['role'] = 'customer'
        user = User.objects.create_user(password=password, **validated_data)
        Customer.objects.create(user=user, customer_id=f"CUST{user.id:06d}")
        return user

class StaffRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=False, allow_null=True)
    pan_number = serializers.CharField(required=True)
    aadhar_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone', 'branch', 'pan_number', 'aadhar_number']
        read_only_fields = ['id']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_pan_number(self, value):
        if not value or len(value) != 10:
            raise serializers.ValidationError("PAN number must be exactly 10 characters.")
        return value.upper()

    def validate_aadhar_number(self, value):
        if not value or not value.isdigit() or len(value) != 12:
            raise serializers.ValidationError("Aadhar number must contain exactly 12 digits.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['role'] = 'staff'
        user = User.objects.create_user(password=password, **validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['role'] = self.user.role
        data['branch'] = self.user.branch.name if getattr(self.user, 'branch', None) else None
        return data

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)
    phone = serializers.CharField(source='user.phone', required=False, allow_blank=True)
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id','user','username','email','first_name','last_name','phone','customer_id','date_of_birth','address','aadhar_number','created_at','can_edit']
        read_only_fields = ['id','created_at']

    def get_can_edit(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        user = request.user
        if user.role == 'admin':
            return True
        if user.role == 'staff':
            if not user.branch:
                return False
            return obj.accounts.filter(branch=user.branch).exists()
        return False

    def validate_phone(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if value and len(value) != 10:
            raise serializers.ValidationError("Phone number must contain 10 digits.")
        return value

    def validate_aadhar_number(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Aadhar number must contain only digits.")
        if value and len(value) != 12:
            raise serializers.ValidationError("Aadhar number must contain 12 digits.")
        return value

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        return super().update(instance, validated_data)

class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'

    def validate_minimum_balance(self, value):
        if value < 0:
            raise serializers.ValidationError("Minimum balance cannot be negative.")
        return value

class AccountSerializer(serializers.ModelSerializer):
    account_type_name = serializers.CharField(source='account_type.name', read_only=True)
    customer_name = serializers.CharField(source='customer.user.username', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = Account
        fields = ['id','customer','customer_name','account_type','account_type_name','branch','branch_name','account_number','balance','status','created_at','updated_at']
        read_only_fields = ['id','balance','created_at','updated_at']

class TransferAccountSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.user.username', read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'account_number', 'customer_name']

class BeneficiarySerializer(serializers.ModelSerializer):
    beneficiary_account_number = serializers.CharField(source='beneficiary_account.account_number', read_only=True)
    beneficiary_name = serializers.CharField(source='beneficiary_account.customer.user.username', read_only=True)

    class Meta:
        model = Beneficiary
        fields = ['id','customer','beneficiary_account','beneficiary_account_number','beneficiary_name','nickname','is_active','created_at']
        read_only_fields = ['id','created_at']

    def validate(self, data):
        customer = data.get('customer')
        beneficiary_account = data.get('beneficiary_account')
        if customer and beneficiary_account:
            if beneficiary_account.customer == customer:
                raise serializers.ValidationError({'beneficiary_account': 'You cannot add your own account as beneficiary.'})
        return data

class TransactionSerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(source='account.account_number', read_only=True)
    related_account_number = serializers.CharField(source='related_account.account_number', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id','account','account_number','transaction_type','amount','balance_after','reference','description','status','related_account','related_account_number','created_at']
        read_only_fields = ['id','balance_after','reference','status','created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

class StaffListSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'branch', 'branch_name', 'is_active', 'pan_number', 'aadhar_number']

class StaffStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_active']
        read_only_fields = ['id']

class HQVaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = HQVault
        fields = ['id', 'total_balance', 'updated_at']
        read_only_fields = ['id', 'updated_at']

class FundAllocationSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    allocated_by_username = serializers.CharField(source='allocated_by.username', read_only=True)

    class Meta:
        model = FundAllocation
        fields = ['id', 'branch', 'branch_name', 'amount', 'allocated_by', 'allocated_by_username', 'reference', 'created_at']
        read_only_fields = ['id', 'allocated_by', 'reference', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value