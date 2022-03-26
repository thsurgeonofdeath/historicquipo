from django.shortcuts import render, get_object_or_404, redirect
from monument.models import Monument
from monument.forms import AddMonumentForm, UpdateMonumentForm
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Create your views here.

def create_monument_view(request):
	context = {}
	user = request.user
	if not user.is_authenticated or not user.is_admin:
		return redirect("must_admin")

	form = AddMonumentForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		form = AddMonumentForm()
		return redirect("home")

	context['form'] = form

	return render(request,"monument/create_monument.html",context)


def detail_monument_view(request, slug):
	context={}
	user = request.user
	isSaved = False
	
	monument = get_object_or_404(Monument, slug=slug)
	if monument.saved.filter(id= request.user.id).exists():
		isSaved = True

	# folium map
	latitude = monument.latitude
	longitude = monument.longitude
	pointA = (latitude,longitude)
	tooltip = monument.title
	m = folium.Map(width=600,height=400,location=pointA, zoom_start=14)
	folium.Marker([latitude,longitude],tooltip=tooltip,icon=folium.Icon(color='red',icon='cloud')).add_to(m)
	m = m._repr_html_()

	context['monument'] = monument
	context['user'] = user
	context['map'] = m
	context['isSaved'] = isSaved

	return render(request,"monument/detail_monument.html",context)

def edit_monument_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated or not user.is_admin:
		return redirect("must_admin")

	monument = get_object_or_404(Monument, slug=slug)

	if request.POST:
		form = UpdateMonumentForm(request.POST or None, request.FILES or None, instance=monument)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Changements enregistrés"
			monument = obj

	form = UpdateMonumentForm(
			initial = {
					"title": monument.title,
					"description": monument.description,
					"image": monument.image,
					"year":monument.year,
					"city":monument.city,
			}
		)

	context['monument'] = monument
	context['form'] = form
	return render(request,"monument/edit_monument.html",context)



def delete_monument_view(request, slug):
	context={}

	user = request.user
	if not user.is_authenticated or not user.is_admin:
		return redirect("must_admin")

	monument = get_object_or_404(Monument, slug=slug)
	context['monument'] = monument

	if request.method == "POST" : 
		monument.delete()
		return redirect("home")

	return render(request,"monument/delete_monument.html",context)


#function to save/unsave monuments from inside monument details
def saved_monument_view(request, slug):
	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	monument = get_object_or_404(Monument, slug=slug)
	if monument.saved.filter(id= request.user.id).exists():
		monument.saved.remove(request.user)
	else:
		monument.saved.add(request.user)

	return HttpResponseRedirect(request.META['HTTP_REFERER'])




def get_monument_queryset(query=None):
	queryset = []
	queries = query.split(" ")
	for q in queries:
		monuments = Monument.objects.filter(
				Q(title__icontains=q) | 
				Q(year__icontains=q) |
				Q(city__icontains=q)
			).distinct()

		for monument in monuments:
			queryset.append(monument)

	return list(set(queryset))


#function to unsave monuments inside saved list:
def unsave_monument(request, slug):

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	monument = get_object_or_404(Monument, slug=slug)
	if monument.saved.filter(id= request.user.id).exists():
		monument.saved.remove(request.user)

	return HttpResponseRedirect(request.META['HTTP_REFERER'])