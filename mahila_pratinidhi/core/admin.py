from django.contrib import admin
from core.models import Province, ProvinceMahilaPratinidhiForm, MahilaPratinidhiForm, District, RastriyaShava, PratinidhiShava

admin.site.register(Province)
admin.site.register(ProvinceMahilaPratinidhiForm)
admin.site.register(District)
admin.site.register(MahilaPratinidhiForm)
admin.site.register(RastriyaShava)
admin.site.register(PratinidhiShava)

