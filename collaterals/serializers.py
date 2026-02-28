from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Borrower, Loan, Collateral, CollateralChangeLog


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class BorrowerSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Borrower
        fields = [
            'id',
            'created_by',
            'customer_name',
            'credit_rating',
            'sector',
            'date_added',
            'last_updated'
        ]


class LoanSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    borrower_name = serializers.ReadOnlyField(source='borrower.customer_name')

    class Meta:
        model = Loan
        fields = [
            'id',
            'created_by',
            'borrower',
            'borrower_name',
            'loan_amount',
            'start_date',
            'maturity_date',
            'date_added',
            'last_updated'
        ]


class CollateralSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    loan_details = serializers.SerializerMethodField()
    ltv_ratio = serializers.SerializerMethodField()
    ltv_risk = serializers.SerializerMethodField()

    class Meta:
        model = Collateral
        fields = [
            'id',
            'created_by',
            'loan',
            'loan_details',
            'asset_type',
            'valuer_name',
            'market_value',
            'status',
            'ltv_ratio',
            'ltv_risk',
            'date_added',
            'last_updated'
        ]

    def get_loan_details(self, obj):
        return {
            'loan_id': obj.loan.id,
            'borrower': obj.loan.borrower.customer_name,
            'loan_amount': str(obj.loan.loan_amount)
        }

    def get_ltv_ratio(self, obj):
        return obj.ltv_ratio()

    def get_ltv_risk(self, obj):
        return obj.ltv_risk()


class CollateralChangeLogSerializer(serializers.ModelSerializer):
    changed_by = serializers.ReadOnlyField(source='changed_by.username')
    collateral_details = serializers.SerializerMethodField()

    class Meta:
        model = CollateralChangeLog
        fields = [
            'id',
            'collateral',
            'collateral_details',
            'changed_by',
            'old_value',
            'new_value',
            'old_status',
            'new_status',
            'note',
            'changed_at'
        ]

    def get_collateral_details(self, obj):
        return {
            'asset_type': obj.collateral.get_asset_type_display(),
            'loan_id': obj.collateral.loan.id
        }