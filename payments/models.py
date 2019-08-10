import decimal
from decimal import Decimal

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

        amount_map = {}
        map_total = Decimal(0)
        with decimal.localcontext(decimal.Context(rounding=decimal.ROUND_HALF_UP)):
            for holder in AccountHolder.objects.all():
                if self.recordshare_set.filter(
                        account_holder__reference=holder.reference).exists():
                    amount_map[holder.reference] = round(Decimal(self.recordshare_set.get(
                        account_holder__reference=holder.reference).share / 100) * self.amount, 2)
                else:
                    amount_map[holder.reference] = round(Decimal((100 - sum_shares) / (
                            holder_count - valid_share_count)) / 100 * self.amount, 2)

                map_total += amount_map[holder.reference]

        if map_total != self.amount:
            rounding_victim = AccountHolder.objects.get_rounding_victim()
            amount_map[rounding_victim.reference] += (self.amount - map_total)

        return amount_map

    def find_share(self, reference):
        share_entity = self.recordshare_set.filter(account_holder__reference=reference).first()
        return share_entity.share if share_entity else None

    class Meta:
        ordering = ['-unique_id']


class AccountHolderManager(models.Manager):
    def get_rounding_victim(self):
        return self.order_by('rounding_likelihood', 'name', 'reference').first()


class AccountHolder(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    reference = models.CharField(max_length=4, null=False, blank=False, primary_key=True)
    starting_balance = models.DecimalField(null=False, blank=False, max_digits=10, decimal_places=2, default=0)
    rounding_likelihood = models.PositiveSmallIntegerField(null=True, blank=True, unique=True)

    objects = AccountHolderManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class RecordShare(models.Model):
    bank_record = models.ForeignKey(BankRecord, on_delete=models.CASCADE)
    account_holder = models.ForeignKey(AccountHolder, on_delete=models.CASCADE)
    share = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                             null=False, blank=False)

    class Meta:
        unique_together = (('bank_record', 'account_holder'),)

    def __str__(self):
        return f'{self.share}% {self.account_holder}'
