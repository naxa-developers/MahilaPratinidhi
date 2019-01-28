from django import template

from core.models import District, MahilaPratinidhiForm, BOOL_CHOICES
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.simple_tag
def status(district_id, force_update=False):
    district = District.objects.get(id=district_id)
    total = MahilaPratinidhiForm.objects.filter(district=district).count()
    complete = MahilaPratinidhiForm.objects.filter(district=district, status=True).count()
    incomplete = MahilaPratinidhiForm.objects.filter(district=district, status=False).count()
    if complete == total and total > 0:
        return True
    else:
        return False


@register.simple_tag
def status_complete_count(district_id, force_update=False):
    district = District.objects.get(id=district_id)
    total = MahilaPratinidhiForm.objects.filter(district=district).count()
    complete = MahilaPratinidhiForm.objects.filter(district=district, status=True).count()

    return complete


@register.simple_tag
def available_elected_women(district_id, force_update=False):
    district = District.objects.get(id=district_id)
    total = MahilaPratinidhiForm.objects.filter(district=district).count()

    return total


@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)


@register.filter
def content_type(obj):
    if not obj:
        return False
    return ContentType.objects.get_for_model(obj)


@register.filter
def space_to_underscore(obj):
    return obj.replace(" ", "_")