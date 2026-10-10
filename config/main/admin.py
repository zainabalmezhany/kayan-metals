from django.contrib import admin
from django.utils.html import format_html

from .models import CompanyInfo, ContactRequest, Project, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'short_description', 'full_description')
    list_filter = ('is_active',)
    ordering = ('order', 'title')

    @admin.display(description='معاينة الصورة')
    def image_preview(self, obj):
        if not obj.image:
            return 'لا توجد صورة'
        return format_html('<img src="{}" style="max-height: 48px; max-width: 80px;" />', obj.image.url)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'location', 'completion_date', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'location', 'description')
    ordering = ('order', '-completion_date')

    @admin.display(description='معاينة الصورة')
    def image_preview(self, obj):
        if not obj.image:
            return 'لا توجد صورة'
        return format_html('<img src="{}" style="max-height: 48px; max-width: 80px;" />', obj.image.url)


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service', 'created_at', 'is_processed')
    list_editable = ('is_processed',)
    list_filter = ('is_processed', 'created_at', 'service')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_processed']

    def mark_processed(self, request, queryset):
        queryset.update(is_processed=True)

    mark_processed.short_description = 'تحديد كمعالجة'


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone_1', 'phone_2', 'email')
    fieldsets = (
        ('بيانات الشركة', {
            'fields': ('company_name', 'address_riyadh', 'working_hours')
        }),
        ('معلومات الاتصال', {
            'fields': (
                'phone_1',
                'phone_2',
                'whatsapp_1',
                'whatsapp_2',
                'email',
            )
        }),
        ('روابط التواصل الاجتماعي', {
            'fields': ('facebook_url', 'tiktok_url', 'instagram_url', 'whatsapp_url')
        }),
        ('خرائط Google', {
            'fields': ('google_maps_embed_url',)
        }),
    )

    def has_add_permission(self, request):
        return not CompanyInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
