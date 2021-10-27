from django.contrib import admin
from .models import Roles, Shift, Student, Timesheet

# Register your models here.
admin.site.register(Roles)
# admin.site.register(Shift)
admin.site.register(Student)
admin.site.register(Timesheet)

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('studentID', 'date', 'role', 'startHour', 'endHour', 'payment')     #column titles showed
    ordering = ('date',)