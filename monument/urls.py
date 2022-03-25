from django.urls import path
from monument.views import create_monument_view,detail_monument_view, edit_monument_view, delete_monument_view, saved_monument_view, get_monument_queryset, unsave_monument

app_name='monument'

urlpatterns = [
	path('create/',create_monument_view, name="create"),
	path('<slug>/',detail_monument_view, name="detail"),
	path('<slug>/edit',edit_monument_view, name="edit"),
	path('<slug>/delete',delete_monument_view, name="delete"),
	path('<slug>/save', saved_monument_view, name="saving"),
	 path('<slug>/unsave/',unsave_monument,name="unsave"),

]