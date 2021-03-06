import locale
from decimal import Decimal

from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaulttags import register
from django.templatetags.static import static


def accounting(value, arg):
    locale.setlocale(locale.LC_MONETARY, 'en_NZ.UTF-8')
    separated = f'{value:n}'
    return separated


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key) if type(dictionary) is dict else None


@register.inclusion_tag('payments/_amount_cell.html')
def amount_cell(amount):
    is_decimal = isinstance(amount, Decimal)
    return {
        'amount': (
            '{0:,.2f}'.format(amount) if amount >= 0 else '({0:,.2f})'.format(abs(amount))) if is_decimal else amount,
        'is_negative': is_decimal and amount < 0
    }


@register.filter
def currency(dollars):
    dollars = round(float(dollars), 2)
    return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])


@register.simple_tag
def share_map_value(share_map, record, holder):
    return share_map.get(share_map_key(record, holder)) or ''


@register.simple_tag
def share_map_key(record, holder):
    return f'{record.unique_id}_{holder.reference}'


@register.simple_tag
def holder_image(holder_name, suffix=None):
    return static(f'payments/material-letters/{holder_name[:1]}{suffix if suffix else ""}.png')


@register.inclusion_tag('payments/_share_display.html')
def share_display(share_map, record, holder):
    return {'share_value': share_map_value(share_map, record, holder)}


@register.inclusion_tag('payments/_total_verification.html')
def total_verification(total_map):
    return {'difference': 0}
