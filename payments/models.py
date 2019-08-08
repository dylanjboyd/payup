from django.db import models


class BankRecord(models.Model):
    date_processed = models.DateField(null=False, blank=False)
    date_transaction = models.DateField(null=False, blank=False)
    unique_id = models.CharField(null=False, blank=False, unique=True, max_length=10, primary_key=True)
    tran_type = models.CharField(null=False, blank=False, max_length=15)
    reference = models.CharField(null=False, blank=False, max_length=4)
    description = models.CharField(null=False, blank=False, max_length=200)
    amount = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2)
