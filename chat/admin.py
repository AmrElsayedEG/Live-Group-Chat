from django.contrib import admin
from chat.models.room import Room

class RoomAdmin(admin.ModelAdmin):

    search_fields = ('name',)
    list_display = ('name', 'current_users',)


admin.site.register(Room, RoomAdmin)
