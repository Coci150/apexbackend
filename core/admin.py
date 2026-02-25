from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count
from .models import Contact
import datetime


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = ('name', 'email', 'company', 'created_at', 'message_preview')

    # Add filters in sidebar
    list_filter = ('created_at', 'company')

    # Enable search
    search_fields = ('name', 'email', 'company', 'message')

    # Default sorting
    ordering = ('-created_at',)

    # Make fields read-only
    readonly_fields = ('created_at',)

    # Date hierarchy for easy navigation
    date_hierarchy = 'created_at'

    # Number of items per page
    list_per_page = 25

    # Custom method to show message preview
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message

    message_preview.short_description = 'Message Preview'

    # Actions dropdown
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="campaign_messages.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Company', 'Message', 'Date'])

        for obj in queryset:
            writer.writerow([obj.name, obj.email, obj.company, obj.message, obj.created_at])

        return response

    export_as_csv.short_description = "Export selected to CSV"

    # ----- NEW: Statistics Dashboard URLs -----
    def get_urls(self):
        # Get the default admin URLs
        urls = super().get_urls()

        # Add custom URLs
        custom_urls = [
            path('campaign-stats/',
                 self.admin_site.admin_view(self.campaign_stats_view),
                 name='campaign-stats'),
        ]

        # Return custom URLs + default URLs
        return custom_urls + urls

    # ----- NEW: Statistics Dashboard View -----
    def campaign_stats_view(self, request):
        """Display campaign statistics dashboard"""

        # Get basic statistics
        total_messages = Contact.objects.count()

        # Today's messages
        today = datetime.date.today()
        messages_today = Contact.objects.filter(created_at__date=today).count()

        # This week's messages
        from django.utils import timezone
        week_start = timezone.now() - datetime.timedelta(days=timezone.now().weekday())
        messages_this_week = Contact.objects.filter(created_at__gte=week_start).count()

        # This month's messages
        month_start = timezone.now().replace(day=1)
        messages_this_month = Contact.objects.filter(created_at__gte=month_start).count()

        # Top companies (excluding empty ones)
        top_companies = Contact.objects.exclude(company_exact='').exclude(company_isnull=True).values(
            'company').annotate(
            count=Count('company')
        ).order_by('-count')[:10]

        # Messages by date (last 30 days)
        last_30_days = timezone.now() - datetime.timedelta(days=30)
        daily_stats = Contact.objects.filter(
            created_at__gte=last_30_days
        ).extra(
            {'date': "date(created_at)"}
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        # Messages by hour (to see peak times)
        hourly_stats = Contact.objects.extra(
            {'hour': "strftime('%H', created_at)"}
        ).values('hour').annotate(
            count=Count('id')
        ).order_by('hour')

