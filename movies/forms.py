from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    comment = forms.CharField(max_length=140)
    class Meta:
        model = Rating
        SCORE = ((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),)
        fields = ['score', 'comment',]
        
        widgets  = {
            'score': forms.Select(choices=SCORE)
        }