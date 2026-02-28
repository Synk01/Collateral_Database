from django.contrib import admin
from .models import Borrower, Loan, Collateral, CollateralChangeLog

# Registering models makes them visible and manageable
# in Django's built-in admin panel at /admin/
admin.site.register(Borrower)
admin.site.register(Loan)
admin.site.register(Collateral)
admin.site.register(CollateralChangeLog)