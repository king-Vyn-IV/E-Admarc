from django.contrib import admin
from accounts.models import FarmerSubmission  # <-- import from accounts.models

@admin.register(FarmerSubmission)
class FarmerSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    actions = ['approve_submissions', 'reject_submissions']

    def approve_submissions(self, request, queryset):
        queryset.update(status='Approved')
    approve_submissions.short_description = "Approve selected submissions"

    def reject_submissions(self, request, queryset):
        queryset.update(status='Rejected')
    reject_submissions.short_description = "Reject selected submissions"
