import locale

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
