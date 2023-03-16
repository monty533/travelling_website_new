from django.shortcuts import render,redirect
from .forms import RegistrationForm,LoginForm,Profile
from django.contrib import messages
from .models import User
from django.conf import settings
from django.contrib.auth import logout , authenticate , login
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .utils import account_activation_token
import random
# from django.utils.encoding import force_bytes,force_text
# Create your views here.
def home(request):  
    return render(request,'app/home.html')

def registration(request):
    if request.method == 'GET':
        form = RegistrationForm
        return render(request,'app/userregistration.html',{'form':form})
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            ps1 = form.cleaned_data.get('password')
            ps2 = form.cleaned_data.get('confirm_password')
            if ps2 != ps1:
                messages.warning(request,'Password & confirm password must be same')
                return render(request, 'app/userregistration.html', {'form': form})
            elif (len(ps2 or ps1) < 8):
                messages.warning(request,'Length should be 8 of any password')
                return render(request, 'app/userregistration.html', {'form': form})
            else:
                messages.success(request, 'Congratulations!! Registered Successfully')
                form.save()
        return render(request, 'app/userregistration.html', {'form': form})

@login_required
def Password_Change(request):
    if request.method == 'GET':
        return render(request,'app/passwordchange.html')

    if request.method == 'POST':
        # email = request.session['email']
        email = request.user.email
        user = User.objects.get(email=email)
        print('user',user)
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        if not old_password:
            messages.warning(request,'Enter Old Password')
        elif not new_password:
            messages.warning(request,'Enter New Password')
        elif not confirm_new_password:
            messages.warning(request,'Enter Confirm New Password')
        elif new_password != confirm_new_password:
            messages.warning(request,'New password and Confirm Password must be same')
        elif len(old_password) < 8:
            messages.warning(request,'Length should be 8 of old password')
        elif len(new_password) < 8:
            messages.warning(request,'Length should be 8 of new password')
        elif new_password == user.password:
            messages.warning(request,'This Password Already Exist Try New Password')
        else:
            user.password = new_password
            user.save()
            messages.success(request,'Password Change Successfully')
        return render(request,'app/passwordchange.html')
    
def LoginView(request):
    if request.method == 'GET':
        form = LoginForm
        return render(request,'app/login.html',{'form':form})

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if not email:
            messages.info(request,'Email is Required.')
            return redirect('login')
        elif not password:
            messages.info(request,'Password is Required.')
            return redirect('login')
        elif len(password) < 8:
            messages.info(request,'Minimum Length should be 8.')
            return redirect('login')
        user=None
        try:
            user = User.objects.get(email=email)
            if user:
                superuser = user.is_superuser
                if superuser:
                    user = authenticate(email=email,password=password)
                else:
                    user = User.objects.get(email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            
        except Exception as e:
            messages.info(request,'Invalid Credentials, Your Email/Password is wrong.')
            return redirect('login')
       
        return render(request,'app/login.html')

def Forgot_Password(request):
    if request.method == 'GET':
        return render(request,'app/forgotpassword.html')

def Send_Otp(request):
    otp = random.randint(1111,9999)
    email = request.POST.get('email')
    user_email = User.objects.filter(email=email)
    if user_email:
        user = User.objects.get(email=email)
        user.otp = otp
        user.save()
        request.session['email'] = request.POST['email']
        print(otp)
        html_message = "Your one time password : - " + "" + str(otp)
        subject = "Welcome to sartia"
        email_from = settings.EMAIL_HOST_EMAIL
        email_to = [email]
        message = EmailMessage(subject,html_message,email_from,email_to)
        try:
            message.send()
        except Exception as e:
            print(e)
        messages.success(request,'One Time Password Send To Your Email')
        return redirect('enter_otp')
    else:
        if email == "":
            messages.warning(request,"Please Enter Email Address")
        else:
            messages.warning(request,"Invalid email address please enter correct email")
        return render(request,'app/forgotpassword.html')

def Enter_Otp(request):
    if request.session.has_key('email'):
        email = request.session['email']
        user = User.objects.filter(email=email)
        for u in user:
            user_otp = u.otp
        if request.method == 'POST':
            otp = request.POST.get('otp')
            if not otp:
                messages.warning(request,'Otp Is Required')
            elif not user_otp == otp:
                messages.warning(request,'Otp Is Invalid')
            else:
                return redirect('password_reset')

        return render(request,'app/enterotp.html')
    else:
        return render(request,'app/forgotpassword.html')


def Password_Reset(request):
    if request.session.has_key('email'):
        email = request.session['email']
        user = User.objects.get(email=email)
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if not new_password:
                messages.warning(request,'Enter New Password')
            elif not confirm_password:
                messages.warning(request,'Enter Confirm New Password')
            elif new_password == user.password:
                messages.warning(request,'This Password Already Exist Try New Password')
            elif len(new_password) < 8:
                messages.warning(request,'Length should be 8 of new password')
            elif len(confirm_password) < 8:
                messages.warning(request,'Length should be 8 of confirm password')
            elif new_password != confirm_password:
                messages.warning(request,'Both password must be not same')
            else:
                user.password = new_password
                user.save()
                messages.success(request,'Password Change Successfully')
                return redirect('login')

    return render(request,'app/passwordreset.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = Profile()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    
    def post(self,request):
        email = request.user.email
        form = Profile(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            try:
                reg = User.objects.filter(email=email).update(name=name,locality=locality,city=city,zipcode=zipcode)
            except:
                pass
            messages.success(request,'Congratulations!! Profile updated successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})