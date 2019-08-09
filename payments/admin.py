from django.contrib import admin

from payments.models import BankRecord, AccountHolder, RecordShare

admin.site.register(BankRecord)
admin.site.register(AccountHolder)
admin.site.register(RecordShare)
