from django import template
from django.shortcuts import get_object_or_404

from main.models import Test
register = template.Library()


@register.inclusion_tag('tags/test_thumbnail.html')
def test_thumbnail(test_id):
    return {'test': get_object_or_404(Test, id=test_id)}
