import locale

from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaulttags import register


def accounting(value, arg):
    locale.setlocale(locale.LC_MONETARY, 'en_NZ.UTF-8')
    separated = f'{value:n}'
    return separated


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.inclusion_tag('payments/_amount_cell.html')
def amount_cell(amount):
    return {'amount': amount}


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
