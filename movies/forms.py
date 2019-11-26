from django import forms

from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('content', 'score')
