from django.contrib.gis.db import models as gis_models
from django.db import models

# Create your models here.
class Placeholder(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    geometry = gis_models.MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name


class Trailhead(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    location = gis_models.PointField(geography=True, null=True, blank=True)
    elevation = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="trailheads", null=True, blank=True)
    archived = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Trail(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("moderate", "Moderate"),
        ("hard", "Hard")
    ]

    TRAIL_TYPE_CHOICES = [
        ("loop", "Loop"),
        ("out-and-back", "Out & Back"),
        ("point-to-point", "Point to Point"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    trailhead = models.ForeignKey(Trailhead, on_delete=models.CASCADE, related_name="trails")
    distance_miles = models.DecimalField(max_digits=5, decimal_places=2)
    difficulty = models.CharField(max_length=200, choices=DIFFICULTY_CHOICES)
    trail_type = models.CharField(max_length=400, choices=TRAIL_TYPE_CHOICES)
    status = models.CharField(max_length=400, default="open")
    description = models.TextField(blank=True)
    archived = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
