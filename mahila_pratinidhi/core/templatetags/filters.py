from django import template

from core.models import District, MahilaPratinidhiForm, BOOL_CHOICES

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
def status_total_count(district_id, force_update=False):
    district = District.objects.get(id=district_id)
    total = MahilaPratinidhiForm.objects.filter(district=district).count()

    return total