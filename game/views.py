import email
from email.headerregistry import Address
from multiprocessing.forkserver import connect_to_new_process
import random
import re
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from game.models import User,Addgame,Donations,P_game
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)) 

# Create your views here.
def index(request):
    try:
        request.session['email']
        user = User.objects.get(email = request.seession['email'])
        return render(request,'index.html')
    except:
        return render(request,'index.html')

def about(request):
    return render(request,"about.html")
    


def games(request):
    return render(request,"games.html")
    
def news(request):
    return render(request,"news.html")
    
def single(request):
    return render(request,"single.html")

def myprofile(request):
    try:
        user_object = User.objects.get(email = request.session['email'])
        if request.method == 'POST':
            user_object.name = request.POST['name']
            user_object.city = request.POST['city']
            user_object.contact = request.POST['contact']
            if request.FILES:
                user_object.pic = request.FILES['pic']
            user_object.save()
            return render(request, 'myprofile.html',{'user_object':user_object})
        else:
            user_object = User.objects.get(email = request.session['email'])
            return render(request, 'myprofile.html',{'user_object':user_object})
    except:
        return render(request, 'login.html')


def mygame(request):
    user_object = User.objects.get(email = request.session['email'])
    game = Addgame.objects.filter(user = user_object)
    return render(request, 'mygame.html',{'game' : game})

    

def addgame(request):
    if request.method == 'GET':
        return render(request, 'addgame.html' )
    else:
        user_object = User.objects.get(email = request.session['email'])
        Addgame.objects.create(
            title = request.POST['title'],
            user = user_object,
            description = request.POST['description'],
            pic = request.FILES['pic']
        )
        return render(request, 'mygame.html')

def viewgame(request):
    allgame = Addgame.objects.all()
    return render(request, 'viewgame.html', {'allgame':allgame })



def donate(request):
    #payment
    #donation table row create
    #Addgame_object = Addgame.objects.get()
    global amount
    currency = 'INR'
    amount = 50000 # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency, payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    global context
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    # context['single_game'] = Addgame_object
    return render(request, 'donate.html', context = context)


 
 

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            # result = razorpay_client.utility.verify_payment_signature(
            #     params_dict)
            # if result is not None:
            global amount
            amount = 50000  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)

                # render success page on successful caputre of payment
                return render(request, 'pay_success.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'paymentfail.html')
            
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        global user_data
        user_data = {
            'name': request.POST['name'],
            'city' : request.POST['city'],  
            'email': request.POST['email'],
            'contact':request.POST['contact'],
            'password': request.POST['password'],
            'cpassword':request.POST['cpassword']
                }
        if user_data['password'] == user_data['cpassword']:
            global c_otp
            c_otp = random.randint(1000,9999)
            message = f'Hi, your OTP is {c_otp}'
            subject = 'Registration,'
            from_email=settings.EMAIL_HOST_USER
            send_mail(subject,message,from_email,[user_data['email']])
            return render(request,'otp.html',{'msg':'Check Your MailBox'})
        else:
            return render (request,'register.html',{'msg':'Passwords Does Not Match'})    
   

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        try:
            user_data = User.objects.get(email = request.POST['email'])
            if user_data.password == request.POST['password']:
                request.session['email'] = request.POST['email']
                return render(request,'index.html')
            else:
                return render(request,'login.html',{'msg':'wrong password!!!'})
        except:
            return render(request,'login.html',{'msg':'Email does not exist!!!'})

def forgetpass(request):
    if request.method == 'GET':
        return render(request, 'forgetpass.html')
    else:
        u_email = request.POST['email']
        try:
            user_object = User.objects.get(email = u_email)
            subject = 'Account Recovery'
            message = f'Your password is {user_object.password}.'
            from_email = settings.EMAIL_HOST_USER
            rec = [u_email]
            send_mail(subject, message, from_email, rec)
            return render(request, 'login.html')
        except:
            return render(request, 'forgetpass.html', {'msg':'Account does not exist!!!'})
    
    
def logout(request):
    del request.session['email']
    return render(request,'login.html')

def otp(request):
        if request.method == 'POST':
            if c_otp == int(request.POST['uotp']):
                User.objects.create(
                name=user_data['name'],
                city=user_data['city'],
                email=user_data['email'],
                contact=user_data['contact'],
                password=user_data['password']
                )
                return render(request,'index.html',{'msg':'Account SucessFully Created!!!!....'})
            else:
                return render(request,'otp.html',{'msg':'OTP Is worng!!'})
        else:
            return render(request,'login.html')



def contact(request):
    if request.method == 'GET':
        return render(request, 'contact.html' )
    else:
        user_object = User.objects.get(email = request.session['email'])
        global paydata
        paydata = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'phone':request.POST['phone'],
            'city' : request.POST['city'], 
            'message': request.POST['message'], 
        }
        P_game.objects.create(
                name = paydata['name'],
                email = paydata['email'],
                phone = paydata['phone'],
                city = paydata['city'],
                message = paydata['message']
                )
        return render(request,"onlinegame.html")
    
def onlinegame(request):
        return render(request,'onlinegame.html')

def pay_success(request):
    return render(request,'pay_success.html')



    

    
    
    
