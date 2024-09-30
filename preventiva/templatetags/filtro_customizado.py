import re
from datetime import datetime

from django import template

register = template.Library()

@register.filter
def data_br(value):
    if value is None:
        return "00/00/00"
    if len(value) == 10:
        return re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", value)
    return datetime.fromisoformat(value[0:16]).strftime("%d/%m/%y - %H:%Mh")