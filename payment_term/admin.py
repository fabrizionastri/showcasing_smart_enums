from django.contrib import admin
from .models import PaymentTermTemplate

class PaymentTermTemplateAdmin(admin.ModelAdmin):
    pass


admin.site.register(PaymentTermTemplate, PaymentTermTemplateAdmin)