import re
from itertools import product

from django.db.models import Sum
from django.shortcuts import render, redirect
from tablib import Dataset

from payments.models import BankRecord, AccountHolder, RecordShare
from payments.resources import BankRecordResource


def index(request):
    holder_map = {h.reference: h.name for h in AccountHolder.objects.all()}
    record_count = BankRecord.objects.count()
    total_amount = BankRecord.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {'records': BankRecord.objects.all(), 'holders': AccountHolder.objects.all(), 'holder_map': holder_map,
               'record_count': record_count, 'total_amount': total_amount}
    return render(request, 'payments/index.html', context)


def edit(request):
    share_map = get_share_map()

    if request.method == 'POST':
        if 'submit-file' in request.POST:
            uploaded_file = request.FILES.get('record-csv')
            record_resource = BankRecordResource()
            dataset = Dataset()

            uploaded_text = uploaded_file.read().decode('ascii')
            substring_index = uploaded_text.index('Date Processed')
            substring = uploaded_text[substring_index:]
            substring = re.sub(r'(\d{4})/(\d{2})/(\d{2})', r'\g<1>-\g<2>-\g<3>', substring)
            dataset.load(substring)
            result = record_resource.import_data(dataset, dry_run=True)  # Test the data import

            if not result.has_errors():
                record_resource.import_data(dataset, dry_run=False)  # Actually import now

        elif 'submit-shares' in request.POST:
            for share_key, share_value in share_map.items():
                new_share_value = request.POST.get(share_key)
                if not new_share_value:
                    continue

                unique_id, reference = share_key.split('_')
                RecordShare.objects.update_or_create(share=new_share_value,
                                                     defaults={'bank_record_id': unique_id,
                                                               'account_holder_id': reference})

        return redirect('index')

    holder_map = {h.reference: h.name for h in AccountHolder.objects.all()}
    record_count = BankRecord.objects.count()
    total_amount = BankRecord.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {'records': BankRecord.objects.all(), 'holders': AccountHolder.objects.all(), 'holder_map': holder_map,
               'record_count': record_count, 'total_amount': total_amount, 'include_table_buttons': True,
               'share_map': share_map}

    return render(request, 'payments/edit.html', context)


def get_share_map():
    return {f'{r.unique_id}_{h.reference}': r.find_share(r.reference) for
            r, h in product(BankRecord.objects.all(), AccountHolder.objects.all())}
