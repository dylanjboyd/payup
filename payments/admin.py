from django.contrib import admin

from payments.models import BankRecord, RecordMeta, AccountHolder, RecordShare

admin.site.register(BankRecord)
admin.site.register(RecordMeta)
admin.site.register(AccountHolder)
admin.site.register(RecordShare)
