import re
from decimal import Decimal
from itertools import product

from django.db.models import Sum
from django.shortcuts import render, redirect
from tablib import Dataset

from payments.models import BankRecord, AccountHolder, RecordShare
from payments.resources import BankRecordResource


def index(request):
    return render(request, 'payments/index.html', get_shared_context())


def get_shared_context():
    holder_map = {h.reference: h.name for h in AccountHolder.objects.all()}
    record_count = BankRecord.objects.count()
    total_amount = BankRecord.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_map = {h.reference: get_holder_total(h) for h in
                 AccountHolder.objects.all()}
    context = {'records': BankRecord.objects.all(), 'holders': AccountHolder.objects.all(), 'holder_map': holder_map,
               'record_count': record_count, 'total_amount': total_amount, 'total_map': total_map,
               'share_map': get_share_map()}
    return context


def edit(request):
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
                if new_share_value == share_value or not (
                        new_share_value or share_value) or new_share_value > 100 or new_share_value < 1:
                    continue

                unique_id, reference = share_key.split('_')
                if not new_share_value and share_value:
                    RecordShare.objects.get(bank_record_id=unique_id, account_holder_id=reference).delete()
                else:
                    RecordShare.objects.update_or_create(bank_record_id=unique_id,
                                                         account_holder_id=reference,
                                                         defaults={'share': new_share_value})

        return redirect('index')

    context = get_shared_context()
    context['include_table_buttons'] = True

    return render(request, 'payments/edit.html', context)


def get_share_map():
    return {f'{r.unique_id}_{h.reference}': r.find_share(h.reference) for
            r, h in product(BankRecord.objects.all(), AccountHolder.objects.all())}


def get_holder_total(holder):
    total = Decimal(0)
    for record in BankRecord.objects.all():
        total += (record.get_amount_map()[holder.reference] or 0)

    return total
