from django import forms


class GetLocations(forms.Form):
    location1 = forms.CharField(max_length=200, label='First location')
    location2 = forms.CharField(max_length=200, label='Second location')
    location3 = forms.CharField(max_length=200, label='Third location')
    location4 = forms.CharField(max_length=200, label='Fourth location')