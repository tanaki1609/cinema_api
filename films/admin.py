from django.contrib import admin
from .models import Film, Director, Genre, Review


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0


class FilmAdmin(admin.ModelAdmin):
    list_display = 'title director rating release_year created'.split()
    list_editable = 'director'.split()
    inlines = [ReviewInline]


admin.site.register(Film, FilmAdmin)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Review)
