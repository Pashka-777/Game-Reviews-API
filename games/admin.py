from django.contrib import admin
from .models import Game, Review

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title','genre','release_date')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user','game','score','created_at')
