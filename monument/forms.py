from django import forms
from monument.models import Monument

class AddMonumentForm(forms.ModelForm):

	class Meta:
		model = Monument
		fields = ['title','year', 'description', 'image','latitude','longitude','city']

class UpdateMonumentForm(forms.ModelForm):

	class Meta:
		model = Monument
		fields = ['title','year', 'description', 'image','city']

	def save(self, commit=True):
		monument = self.instance
		monument.title = self.cleaned_data['title']
		monument.year = self.cleaned_data['year']
		monument.description = self.cleaned_data['description']

		if self.cleaned_data['image']:
			monument.image = self.cleaned_data['image']

		if commit:
			monument.save()
		return monument

