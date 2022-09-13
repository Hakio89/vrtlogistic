from django.contrib import admin
from xiaomi.models import *
# Register your models here.

admin.site.register(Xiaomi)
admin.site.register(Status)
admin.site.register(XiaomiWaitingParts)
admin.site.register(XiaomiPartsCatalog)
admin.site.register(XiaomiClaimParts)