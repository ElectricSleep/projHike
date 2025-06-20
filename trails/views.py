from django.shortcuts import render
from django.core.serializers import serialize
from .models import Trailhead

def index(request):
    trailheads_geojson = serialize('geojson', Trailhead.objects.all(), geometry_field='location', fields=('name',))
    return render(request, 'trails/index.html', {'trailheads_geojson': trailheads_geojson})
