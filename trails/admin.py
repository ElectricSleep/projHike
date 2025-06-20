from django.contrib import admin
from django.utils.html import format_html
from leaflet.admin import LeafletGeoAdmin
from .models import Region, Trailhead, Trail

# Actions for Trailhead and Trail
def verify_selected(modeladmin, request, queryset):
    updated = queryset.update(verified=True)
    modeladmin.message_user(request, f"{updated} item(s) verified.")
verify_selected.short_description = "Mark selected as Verified"

def unverify_selected(modeladmin, request, queryset):
    updated = queryset.update(verified=False)
    modeladmin.message_user(request, f"{updated} item(s) unverified.")
unverify_selected.short_description = "Mark selected as Unverified"

def archive_selected(modeladmin, request, queryset):
    updated = queryset.update(archived=True)
    modeladmin.message_user(request, f"{updated} item(s) archived.")
archive_selected.short_description = "Mark selected as Archived"

def unarchive_selected(modeladmin, request, queryset):
    updated = queryset.update(archived=False)
    modeladmin.message_user(request, f"{updated} item(s) unarchived.")
unarchive_selected.short_description = "Mark selected as Unarchived"

# Inline for managing Trails inside Trailhead admin
class TrailInline(admin.TabularInline):
    model = Trail
    extra = 1
    fields = ('name', 'distance_miles', 'difficulty', 'trail_type', 'status', 'archived')
    show_change_link = True

@admin.register(Region)
class RegionAdmin(LeafletGeoAdmin):
    list_display = ('name', 'slug', 'is_group_display', 'parent')
    list_filter = ('parent',)
    ordering = ('name',)
    search_fields = ('name',)

    def is_group_display(self, obj):
        return obj.is_group()
    is_group_display.boolean = True
    is_group_display.short_description = 'Grouped Region?'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('parent')

@admin.register(Trailhead)
class TrailheadAdmin(LeafletGeoAdmin):
    list_display = ('name', 'region', 'verified', 'archived')
    list_filter = ('region', 'archived', 'verified')
    ordering = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TrailInline]
    actions = [verify_selected, unverify_selected, archive_selected, unarchive_selected]

@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display = ('name', 'trailhead_link', 'distance_miles', 'difficulty', 'trail_type', 'verified', 'archived')
    list_filter = ('difficulty', 'trail_type', 'status', 'archived')
    ordering = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    actions = [verify_selected, unverify_selected, archive_selected, unarchive_selected]

    # Make trailhead field link to its admin page
    def trailhead_link(self, obj):
        if obj.trailhead:
            url = f"/admin/trails/trailhead/{obj.trailhead.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.trailhead.name)
        return "-"
    trailhead_link.short_description = 'Trailhead'
    trailhead_link.admin_order_field = 'trailhead__name'
