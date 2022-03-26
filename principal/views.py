from django.shortcuts import render, get_object_or_404
from monument.models import Monument
from monument.views import get_monument_queryset
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from operator import attrgetter

# Create your views here.

MONUMENTS_PER_PAGE = 6

def home_screen_view(request):
	context={}
	user = request.user
	
	# search feature
	query = ''
	if request.GET:
		query = request.GET.get('q','')
		context['query'] = str(query)

	context['user'] = user
	monuments = get_monument_queryset(query)

	#pagination feature
	page = request.GET.get('page',1)
	monuments_paginator = Paginator(monuments, MONUMENTS_PER_PAGE)

	try:
		monuments = monuments_paginator.page(page)
	except PageNotAnInteger :
		monuments = monuments_paginator.page(MONUMENTS_PER_PAGE)
	except EmptyPage :
		monuments = monuments_paginator.page(monuments_paginator.num_pages)

	context['monuments'] = monuments
	
	return render(request,"principal/home.html", context)