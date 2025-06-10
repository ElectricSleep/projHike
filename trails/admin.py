from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Region, Trailhead, Trail

# Inline for managing Trails inside Trailhead admin
class TrailInline(admin.TabularInline):  # or use StackedInline for more detail
    model = Trail
    extra = 1
    fields = ('name', 'distance_miles', 'difficulty', 'trail_type', 'status', 'archived')
    show_change_link = True

@admin.register(Region)
class RegionAdmin(LeafletGeoAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Trailhead)
class TrailheadAdmin(LeafletGeoAdmin):
    list_display = ('name', 'slug', 'region', 'archived')
    list_filter = ('region', 'archived')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TrailInline]

@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'trailhead', 'distance_miles', 'difficulty', 'trail_type', 'status', 'archived')
    list_filter = ('difficulty', 'trail_type', 'status', 'archived')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
