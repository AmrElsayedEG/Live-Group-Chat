from django import forms
from chat.models.room import Room

class CreateRoom(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name',]