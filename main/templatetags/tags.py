from django import template
register = template.Library()
import re

@register.filter
def snaturaltime(naturaltime):
    return re.sub(',.*?ago', ' ago', naturaltime)