# AgriMaxApp/templatetags/custom_filters.py
import logging

from django import template

register = template.Library()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug('Custom template tags loaded')


@register.filter(namr='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(namr='get_percent')
def get_percent(obj):
    return obj * 100


@register.filter(name='get_dp')
def get_dp(val):
    return f"{val:.2f}"
