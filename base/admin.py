from django.contrib import admin
from .models import (
    Department,
    Book,
    Visitor,
    Loan,
)

admin.site.register(
    [
        Department,
        Book,
        Visitor,
        Loan
    ]
)
