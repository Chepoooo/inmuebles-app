from django import template

register = template.Library()

@register.filter
def cop(value):

    
    if value is None or value == "":
        return ""

    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    return f"$ {value:,}".replace(",", ".") + " COP"
    
