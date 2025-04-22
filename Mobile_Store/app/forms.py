# tao forms de upload anh tim kiem
from django import forms

class ImageSearchForm(forms.Form):
    image = forms.ImageField(required = True)