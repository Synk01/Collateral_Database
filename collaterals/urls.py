from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    BorrowerListCreateView,
    BorrowerDetailView,
    LoanListCreateView,
    LoanDetailView,
    CollateralListCreateView,
    CollateralDetailView,
    ChangeLogListView
)

urlpatterns = [

    # Auth endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Borrower endpoints
    path('borrowers/', BorrowerListCreateView.as_view(), name='borrower_list'),
    path('borrowers/<int:pk>/', BorrowerDetailView.as_view(), name='borrower_detail'),

    # Loan endpoints
    path('loans/', LoanListCreateView.as_view(), name='loan_list'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan_detail'),

    # Collateral endpoints
    path('collaterals/', CollateralListCreateView.as_view(), name='collateral_list'),
    path('collaterals/<int:pk>/', CollateralDetailView.as_view(), name='collateral_detail'),

    # Change log endpoint
    path('changelogs/', ChangeLogListView.as_view(), name='changelog_list'),
]