from django.contrib import admin
from .models import Contact

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'less_content')
    search_fields = ('name', 'email')

    def less_content(self, obj):
        return obj.content[:100]

admin.site.register(Contact, ContactAdmin)