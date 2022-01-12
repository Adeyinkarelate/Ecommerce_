from django.contrib import messages, auth
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse, render
from account.forms import RegistrationForm
from account.models import Account
from django.contrib.auth.decorators import login_required

#verification email 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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

            #ACCOUNT ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('account/account_verification_email.html', {
                'user':user,
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),    #encoding the user id using the bse64, so nobody can see the primary key
                'token':default_token_generator.make_token(user),

            })
            to_email = email
            send_email = EmailMessage(mail_subject ,message , to=[to_email])
            send_email.send()  
            return redirect('/account/login/?command=verification&email=' + email)
    else:
        form = RegistrationForm()
    context = {
      'form':form
    }
    return render(request , 'account/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid login credentials')
            return redirect('login')
    return render(request , 'account/login.html')

@login_required(login_url = 'login')   #you cant logout if you dont login
def logout(request):
    auth.logout(request)
    messages.success(request,'You have successfully logged out!')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid  = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations your account is activated succefully')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link ')
        return redirect('register')
    return HttpResponse('Ok')
    
@login_required(login_url = 'login')   #you cant logout if you dont login
def dashboard(request):
    return render(request,'account/dashboard.html' )
'''
# __exact is case sensitive , ensure the 
comming email is the same with what we have in the database
'''
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']  
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email) 
            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('account/reset_password_email.html', {
                'user':user,
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),    #encoding the user id using the bse64, so nobody can see the primary key
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject ,message , to=[to_email])
            send_email.send()  
            messages.success(request,'Password reset email has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request,'Account does not exists')
            return redirect('forgotpassword')
    return render(request, 'account/forgotpassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid  = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid 
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link has expire')
        return redirect('login')
    return HttpResponse('the rest page')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)  #you must use set_password to make it work , not just save it inside db
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request , 'Password do not match ')
            return redirect('resetPassword')
    else:
        return render(request , 'account/resetPassword.html')
    