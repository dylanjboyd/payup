from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class BankRecord(models.Model):
    date_processed = models.DateField(null=False, blank=False)
    date_transaction = models.DateField(null=False, blank=False)
    unique_id = models.CharField(null=False, blank=False, unique=True, max_length=10, primary_key=True)
    tran_type = models.CharField(null=False, blank=False, max_length=15)
    reference = models.CharField(null=False, blank=False, max_length=4)
    description = models.CharField(null=False, blank=False, max_length=200)
    amount = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.description


class RecordMeta(models.Model):
    bank_record = models.OneToOneField(BankRecord, on_delete=models.CASCADE)
    acknowledged = models.BooleanField()

    def __str__(self):
        return str(self.bank_record)


class AccountHolder(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    reference = models.CharField(max_length=4, null=False, blank=False)
    starting_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class RecordShare(models.Model):
    record_meta = models.ForeignKey(RecordMeta, on_delete=models.CASCADE)
    account_holder = models.ForeignKey(AccountHolder, on_delete=models.CASCADE)
    share = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                             null=True, blank=True)

    def __str__(self):
        return f'{self.share}% {self.account_holder}'
