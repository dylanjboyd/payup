from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum


class BankRecord(models.Model):
    date_processed = models.DateField(null=False, blank=False)
    date_transaction = models.DateField(null=False, blank=False)
    unique_id = models.CharField(null=False, blank=False, unique=True, max_length=10, primary_key=True)
    tran_type = models.CharField(null=False, blank=False, max_length=15)
    reference = models.CharField(null=False, blank=False, max_length=4)
    description = models.CharField(null=False, blank=False, max_length=200)
    amount = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2)
    acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return self.description

    def get_amount_map(self):
        sum_shares = self.recordshare_set.aggregate(Sum('share'))['share__sum'] or 0
        valid_share_count = self.recordshare_set.filter().count()
        holder_count = AccountHolder.objects.count()
        if self.recordshare_set.none() or sum_shares <= 0 or sum_shares > 100:
            return {h.reference: self.amount if self.reference == h.reference else 0 for h in
                    AccountHolder.objects.all()}
        return {h.reference: self.recordshare_set.get(
            account_holder__reference=h.reference).share / 100 * self.amount if self.recordshare_set.filter(
            account_holder__reference=h.reference).exists() else (100 - sum_shares) / (
                holder_count - valid_share_count) * self.amount for h in
                AccountHolder.objects.all()}

    class Meta:
        ordering = ['-unique_id']


class AccountHolder(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    reference = models.CharField(max_length=4, null=False, blank=False)
    starting_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class RecordShare(models.Model):
    bank_record = models.ForeignKey(BankRecord, on_delete=models.CASCADE)
    account_holder = models.ForeignKey(AccountHolder, on_delete=models.CASCADE)
    share = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                             null=True, blank=True)

    class Meta:
        unique_together = (('bank_record', 'account_holder'),)

    def __str__(self):
        return f'{self.share}% {self.account_holder}'
