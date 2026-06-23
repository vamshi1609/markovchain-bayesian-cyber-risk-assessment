from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *

# Create your views here.
def main_home(request):
    return render(request,'main/main-home.html')

def main_adminlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        userpassword=request.POST.get('password')
        print(username,userpassword)

        if username =="admin" and userpassword == "admin":
            print('suceeeee')
            messages.success(request,"admin successfully login")
            return redirect('admin_dash')
        else:
            messages.error(request,"invalid credentials")
            return redirect('main_adminlogin')
  
    return render(request,'main/main-adminlogin.html')

def main_contact(request):
    return render(request,'main/main-contact.html')

def main_about(request):
    return render(request,'main/main-about.html')

def main_user_login(request):
      if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")

        try:
            print('tryyyyyyyyy')
            data2=UserModel.objects.get(user_email=email,user_password=password)
            request.session['user_id']=data2.user_id
            print('try2222')
            if data2.user_status == 'accepted':
                
                messages.success(request, 'Successfully Login')
                return redirect('user_dashboard')
            elif data2.user_status == 'pending':
                print('pending')
                messages.warning(request, 'Your request is in pending, please wait for until acceptance')
                return redirect('main_user_login')
            elif data2.user_status == 'declined':
                messages.error(request, 'Your request is declined, so you cannot login')
                return redirect('main_user_login')
        except:
            
            messages.warning(request, 'invalid login')
            return redirect('main_user_login')

   
      return render(request,'main/main-user-login.html')

def main_user_register(request):  # sourcery skip: use-named-expression

    if request.method == 'POST':
       username = request.POST.get("name")
       userdob=request.POST.get("date")
       email = request.POST.get("email")
       password = request.POST.get("password")
       contact = request.POST.get("contact")
       occupation = request.POST.get("occupation")
       image = request.FILES["image"]
       print(username,email,password,contact,image,occupation,userdob)
       user=UserModel.objects.create(user_occupation=occupation,user_username=username ,user_dob=userdob, user_email=email , user_password=password , user_contact=contact , user_image=image)
       if user:
            messages.success(request, 'successfully registered')
            return redirect('main_user_login')
       else:
            messages.error(request, 'Invalid registration')
            return redirect('main_user_register')
                    

    return render(request,'main/main-user-register.html')