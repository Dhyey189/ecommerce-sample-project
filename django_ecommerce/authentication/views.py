from django.shortcuts import render, redirect
from authentication.models import User
from authentication.forms import SignupForm,OtpForm
from django.core.mail import send_mail
import random
# Create your views here.




def signup(request):
    
    if request.session.get('user'):
        return redirect('../../../')
    form = SignupForm()
    otp_form = OtpForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            return redirect('../otp/'+str(user.id))
        return render(request,'signup.html' , {'SignupForm' : form,'error' : form.errors})

    return render(request,'signup.html',{'SignupForm' : form})


def otp(request,id = None):
    if request.session.get('user'):
        return redirect('../../../')
    form = SignupForm()
    otp_form = OtpForm()
    user = User.objects.get(id = id)
    if user is None or id is None:
        return redirect('authentication/signup')
    elif request.method == 'POST' and 'verify' in request.POST:
        otp_form = OtpForm(request.POST)
        if otp_form.is_valid() and str(user.otp) == request.POST.get('otp'):
            user.is_verified = True
            user.save()
            # create session
            request.session['user'] = {'name':user.name, 'email':user.email, 'phone_number' : user.phone_number}
            return redirect('../../../')
    else:
        num = random.randint(1000,9999)
        user.otp = num
        user.save()
        send_mail("Otp for login/signup to ecommerce","your otp:"+str(num),"19ceuos145@ddu.ac.in",[user.email])
        print('mail sent to', user.email)
        return render(request,'otp.html',{'OtpForm':otp_form,'email':user.email})

    
def logout(request):
    del request.session['user']
    return redirect('../../../')


def login(request):
    if request.session.get('user'):
        return redirect('../../../')

    if request.method == 'POST':
        try:
            user = User.objects.get(email = request.POST.get('email'))
        except:
            print("User not exist")
            return render(request,'login.html',{'failed' : 'failed'})
        else:
            user.is_verified = True
            user.save()
            return redirect('../otp/'+str(user.id))
    else:
        return render(request,'login.html')