from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
	records=Record.objects.all()
	if request.method == "POST":
		username=request.POST['username']
		password=request.POST['password']

		user=authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged in!")
			return redirect('Home')
		else:
			messages.success(request, "There was an error logging in please try again later")
			return redirect('Home')
	else:
		return render(request, 'Home.html', {'records':records})


def login_user(request):
	pass

def logout_user(request):
	logout(request)
	messages.success(request, "You have been Logged out")
	return redirect('Home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data['username']
			password=form.cleaned_data['password1']
			user=authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome")
			return redirect('Home')
	else:
		form =SignUpForm()
		return render(request, 'register.html', {'form':form})
	return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
	if request.user.is_authenticated:
		customer_record=Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})

	else:
		messages.success(request, "You Must Be logged in The view that Page...")
		return redirect('Home')

def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_item=Record.objects.get(id=pk)
		delete_item.delete()
		messages.success(request, "Record successfully deleted... ")
		return redirect('Home')
	else:
		messages.success(request, "You must be logged in to be able to delete")
		return redirect('Home')

def add_record(request):
	form=AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method=="POST":
			if form.is_valid():
				add_record=form.save()
				messages.success(request, "Record Added...")
				return redirect("Home")
		return render(request, 'add_record.html', {"form":form})
	else:
		messages.success(request, "You must be logged in...")
		return redirect('Home')
	return render(request, 'add_record.html', {})

def update_record(request, pk):
	if request.user.is_authenticated:
		current_record=Record.objects.get(id=pk)
		form=AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('Home')
		return render(request, "update_record.html", {"form":form})
	else:
		messages.success(request, "You must be Logged In...")
		return redirect("Home")
