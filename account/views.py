from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from account.forms import *
from account.models import Account
from monument.models import Monument
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# Create your views here.
def registration_view(request):
	context={}

	user = request.user
	if user.is_authenticated :
		return redirect ("home")

	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email 		= form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email,password=raw_password)
			login(request,account)
			return redirect('home')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm();
		context['registration_form'] = form

	return render(request, 'account/register.html', context)

def logout_view(request):
	logout(request)
	return redirect('home')

def login_view(request):

	context = {}
	user = request.user
	if user.is_authenticated: 
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "account/login.html", context)

def account_view(request):
	context={}
	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	context['user'] = user
	return render(request,"account/compte.html",context)

def account_edit(request):
	if not request.user.is_authenticated:
		return redirect("must_authenticate")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
					"phone": request.POST["phone"],
			}
			form.save()
			context['success_message'] = "Successful!"
	else:
		form = AccountUpdateForm(
			initial={
					"email": request.user.email, 
					"username": request.user.username,
					"phone": request.user.phone
				}
			)

	context['account_form'] = form

	return render(request, "account/edit.html", context)



def account_saved(request):
	context={}
	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	savedlist = Monument.objects.filter(saved = request.user)

	context['savedlist'] = savedlist

	return render(request,"account/saved.html",context)

def about_us_view(request):
	context={}
	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	users = Account.objects.all()

	context['users'] = users
	return render(request,"account/aboutus.html",context)


def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})


def must_admin_view(request):
	return render(request, 'account/must_admin.html', {})

def users_table_view(request):
	context = {}
	user = request.user
	if not user.is_authenticated or not user.is_admin:
		return redirect("must_admin")

		
	users = Account.objects.filter(is_admin=False)
	context['users'] = users
	return render(request, 'account/users_table.html', context)