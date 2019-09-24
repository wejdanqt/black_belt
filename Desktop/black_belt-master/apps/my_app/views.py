from django.shortcuts import render, HttpResponse,redirect
from .models import User , Record
from django.contrib import messages
import bcrypt
from django.core.mail import send_mail


#My Import 
import re


def index(request):
    return render(request,"my_app/index.html")

def index2(request):
    msg=''
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
            # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
                print("dfghjhhhhhhhhhhhhhhhh", value)
                msg+=value+"\n"
        else:           
            name=request.POST["name"]
            email=request.POST["email"]
            password=request.POST["password"]
            hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(name=name, email=email, password=hash1)

    context={
        "users":User.objects.all(),
        "msg": msg
    }
    emails=User.objects.values('email')
    print(emails)
    # for email in emails:
    #     print(email.email)


    #print(User.objects.all().values())  
    return render(request,"my_app/login.html",context)

def contact(request):
    return render(request,"my_app/contact.html")

def records(request):
    return render(request,"my_app/records.html")

def check(request):
    return render(request,"my_app/check.html")



def login(request):
    user = User.objects.get(email=request.POST['email'])
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):  
        print("password match")
    else:
        print("failed password")

    return render(request,"my_app/home.html")


def admin(request):
    context={}
    if User.objects.filter(active=False).exists():
            unacitvated=User.objects.filter(active=False)
        
        
    if User.objects.filter(active=True).exists():        
        acitvated=User.objects.filter(active=True)
        

    context={
        "acitvated":acitvated,
        "unacitvated":unacitvated
    }
    print(context)
    return render(request,"my_app/admin.html", context)
    
def activate(request,id):
    user=User.objects.get(id=id)
    user.actived=True
    user.save()
    return redirect("/admin")
    
def deactivate(request,id):
    user=User.objects.get(id=id)
    user.actived=False
    user.save()
    return redirect("/admin")


 #My Code for uploading a CSV file 

def upload_csv(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            print("not CSV")
            messages.error(request,'File is not CSV type. Please upload a CSV file')
            return redirect("/check")
         
        else:
            #Trying to send email to the user mail box
            #Send email to the user by using the session
            user = User.objects.get(id=1)
            send_mail('This is an Email form Customer Satisfaction Tool' , 'Prosess is succeed', 
            'customer.satisfaction.sa@gmail.com' , [user.email],
            fail_silently=False)
            #.........................
          
            file_data = csv_file.read().decode("utf-8")	
            lines = file_data.split("\n")
            #We need to add id sesstion for the user for now i will assign to static with user id = 1 
            this_user = User.objects.get(id=1)
            
            for line in lines:						
                fields = line.split(",")
                n = re.sub('\W+',' ', fields[0] )
                a = re.sub('\W+',' ', fields[1] )

                #It is one to many
                Record.objects.create(name= n ,acount = '@' + a , user = this_user )

            return redirect("/check")



    