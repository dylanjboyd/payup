from import_export import resources
from import_export.fields import Field

from .models import BankRecord


class BankRecordResource(resources.ModelResource):
    date_processed = Field(attribute='date_processed', column_name='Date Processed')
    date_transaction = Field(attribute='date_transaction', column_name='Date of Transaction')
    unique_id = Field(attribute='unique_id', column_name='Unique Id')
    tran_type = Field(attribute='tran_type', column_name='Tran Type')
    reference = Field(attribute='reference', column_name='Reference')
    description = Field(attribute='description', column_name='Description')
    amount = Field(attribute='amount', column_name='Amount')

    class Meta:
        model = BankRecord
        skip_unchanged = True
        report_skipped = False
