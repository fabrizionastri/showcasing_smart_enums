from django.contrib import admin
from .models import Commitment

class CommitmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Commitment, CommitmentAdmin)