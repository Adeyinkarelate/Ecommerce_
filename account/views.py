from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse, render
from account.forms import RegistrationForm
from account.models import Account

# Create your views here.
# when u use django form, we use clean data to ferch the value from the request
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]   #generating username ourself, we dont want user to create it 

            # we cant put phone number in the create_user bcs we create it seprately 
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username = username)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Registration successful.')
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
      'form':form
    }
    return render(request , 'account/register.html',context)

def login(request):
    return render(request , 'account/login.html')

def logout(request):
    return 