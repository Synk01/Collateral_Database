from django.db import models
from django.contrib.auth.models import User

class Borrower(models.Model):
    CREDIT_RATING_CHOICES = [
        ('AAA', 'AAA'), ('AA', 'AA'), ('A', 'A'),
        ('BBB', 'BBB'), ('BB', 'BB'), ('B', 'B'),
        ('CCC', 'CCC'), ('D', 'D'),
    ]
    SECTOR_CHOICES = [
        ('agriculture', 'Agriculture'),
        ('manufacturing', 'Manufacturing'),
        ('real_estate', 'Real Estate'),
        ('retail', 'Retail'),
        ('finance', 'Finance'),
        ('other', 'Other'),
    ]
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    credit_rating = models.CharField(max_length=10, choices=CREDIT_RATING_CHOICES)
    sector = models.CharField(max_length=100, choices=SECTOR_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name


class Loan(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateField()
    maturity_date = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loan #{self.pk} - {self.borrower.customer_name}"


class Collateral(models.Model):
    ASSET_TYPE_CHOICES = [
        ('property', 'Property'),
        ('vehicle', 'Vehicle'),
        ('equipment', 'Equipment'),
        ('land', 'Land'),
        ('stocks', 'Stocks'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('released', 'Released'),
        ('foreclosed', 'Foreclosed'),
    ]
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPE_CHOICES)
    valuer_name = models.CharField(max_length=200)
    market_value = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_asset_type_display()} - Loan #{self.loan.pk}"

    def ltv_ratio(self):
        if self.market_value > 0:
            ratio = (self.loan.loan_amount / self.market_value) * 100
            return round(ratio, 2)
        return None

    def ltv_risk(self):
        ltv = self.ltv_ratio()
        if ltv is None:
            return 'Unknown'
        elif ltv <= 60:
            return 'Low Risk'
        elif ltv <= 80:
            return 'Medium Risk'
        else:
            return 'High Risk'


class CollateralChangeLog(models.Model):
    collateral = models.ForeignKey(
        Collateral,
        on_delete=models.CASCADE,
        related_name='changes'
    )
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    old_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    new_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20, blank=True)
    note = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Change on Collateral #{self.collateral.pk} at {self.changed_at}"