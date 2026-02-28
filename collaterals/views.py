from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Borrower, Loan, Collateral, CollateralChangeLog
from .serializers import (
    RegisterSerializer,
    BorrowerSerializer,
    LoanSerializer,
    CollateralSerializer,
    CollateralChangeLogSerializer
)


# -----------------------------------------------
# CUSTOM PERMISSION
# Users can only edit/delete their own records
# -----------------------------------------------
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user


# -----------------------------------------------
# REGISTER VIEW
# -----------------------------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------------------------------
# BORROWER VIEWS
# -----------------------------------------------
class BorrowerListCreateView(generics.ListCreateAPIView):
    serializer_class = BorrowerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['customer_name', 'sector']
    ordering_fields = ['customer_name', 'date_added']

    def get_queryset(self):
        return Borrower.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BorrowerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BorrowerSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Borrower.objects.filter(created_by=self.request.user)


# -----------------------------------------------
# LOAN VIEWS
# -----------------------------------------------
class LoanListCreateView(generics.ListCreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['borrower__customer_name']
    ordering_fields = ['loan_amount', 'date_added', 'maturity_date']

    def get_queryset(self):
        return Loan.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Loan.objects.filter(created_by=self.request.user)


# -----------------------------------------------
# COLLATERAL VIEWS
# This is the most important view today
# It automatically logs changes when collateral
# value or status is updated
# -----------------------------------------------
class CollateralListCreateView(generics.ListCreateAPIView):
    serializer_class = CollateralSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'asset_type']
    search_fields = ['valuer_name', 'loan__borrower__customer_name']
    ordering_fields = ['market_value', 'date_added']

    def get_queryset(self):
        queryset = Collateral.objects.filter(created_by=self.request.user)

        ltv_risk = self.request.query_params.get('ltv_risk', None)
        if ltv_risk:
            matching_ids = [c.id for c in queryset if c.ltv_risk() == ltv_risk]
            queryset = Collateral.objects.filter(id__in=matching_ids)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CollateralDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CollateralSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Collateral.objects.filter(created_by=self.request.user)

    # This method runs automatically when a collateral is updated
    def perform_update(self, serializer):

        # Get the old values BEFORE saving
        old_collateral = self.get_object()  
        old_value = old_collateral.market_value
        old_status = old_collateral.status

        # Save the new values
        instance = serializer.save()

        # Get the new values AFTER saving
        new_value = instance.market_value
        new_status = instance.status

        # Only create a log if something actually changed
        if old_value != new_value or old_status != new_status:
            CollateralChangeLog.objects.create(
                collateral=instance,
                changed_by=self.request.user,
                old_value=old_value,
                new_value=new_value,
                old_status=old_status,
                new_status=new_status,
                note=f"Updated by {self.request.user.username}"
            )


# -----------------------------------------------
# CHANGE LOG VIEW
# Shows full history of all collateral changes
# -----------------------------------------------

class ChangeLogListView(generics.ListAPIView):
    serializer_class = CollateralChangeLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['collateral']
    ordering_fields = ['changed_at']
    ordering = ['-changed_at']

    def get_queryset(self):
        return CollateralChangeLog.objects.filter(
            collateral__created_by=self.request.user
        )