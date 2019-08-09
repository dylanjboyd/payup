import locale


def accounting(value, arg):
    locale.setlocale(locale.LC_MONETARY, 'en_NZ.UTF-8')
    separated = f'{value:n}'
    return separated
