from django import template

register = template.Library()


##FORMATO DE PESOS CHILENO PARA PRECIOS Y DESCUENTOS
@register.filter
def currency(value):
    return f'{value:,.0f}'.replace(',', '.')