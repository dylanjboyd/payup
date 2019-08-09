from django.shortcuts import render

from payments.models import BankRecord, AccountHolder


def index(request):
    context = {'records': BankRecord.objects.all(), 'holders': AccountHolder.objects.all()}
    return render(request, 'payments/index.html', context)
