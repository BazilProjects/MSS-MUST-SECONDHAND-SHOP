from django import template

register = template.Library()

@register.filter
def format_whatsapp(phone):
    phone = str(phone)
    if len(phone) == 12 and phone.startswith("256"):
        return f"+{phone}"
    if len(phone) >= 10:
        return f"+256{phone[-9:]}"
    return ""
