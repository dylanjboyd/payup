import re

from django.db.models import Sum
from django.shortcuts import render
from tablib import Dataset

from payments.models import BankRecord, AccountHolder
from payments.resources import BankRecordResource


def index(request):
    if request.method == 'POST':
        record_resource = BankRecordResource()
        dataset = Dataset()
        uploaded_file = request.FILES['record-csv']
        uploaded_text = uploaded_file.read().decode('ascii')
        substring_index = uploaded_text.index('Date Processed')
        substring = uploaded_text[substring_index:]
        substring = re.sub(r'(\d{4})/(\d{2})/(\d{2})', r'\g<1>-\g<2>-\g<3>', substring)
        dataset.load(substring)
        result = record_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            record_resource.import_data(dataset, dry_run=False)  # Actually import now

    holder_map = {h.reference: h.name for h in AccountHolder.objects.all()}
    record_count = BankRecord.objects.count()
    total_amount = BankRecord.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {'records': BankRecord.objects.all(), 'holders': AccountHolder.objects.all(), 'holder_map': holder_map,
               'record_count': record_count}
    return render(request, 'payments/index.html', context)
