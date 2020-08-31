from django.shortcuts import render 
import pyrebase
from pyrebase import initialize_app
from Crypto.PublicKey import RSA
from django.contrib import auth


firebaseConfig = {
    'apiKey': "AIzaSyBy8QM7yfpzHtZtw4GZ4Yivce3d-sOL_Q4",
    'authDomain': "ccswebpage-faf52.firebaseapp.com",
    'databaseURL': "https://ccswebpage-faf52.firebaseio.com",
    'projectId': "ccswebpage-faf52",
    'storageBucket': "ccswebpage-faf52.appspot.com",
    'messagingSenderId': "434868257619",
    'appId': "1:434868257619:web:107c16afba3c41422bd7a6",
    'measurementId': "G-6GWMR5MVX7"
  }
  
firebase = pyrebase.initialize_app(firebaseConfig)
  
authe = firebase.auth()
database= firebase.database()
def signIn(request):
    return render (request, "signIn.html")

def postsign(request):
  
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
      user = authe.sign_in_with_email_and_password(email,passw)
    except:
      message="Invalid Credentials"
      return render(request,"signIn.html",{"messg":message})
    print(user ['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render (request, "welcome.html",{"e":name})

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')

def signUp(request):

    return render(request,'signup.html')

def postsignup(request):

    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user=authe.create_user_with_email_and_password(email,passw)
    except:
        message="Unable to create Account. Id already registered OR Password too weak."
        return render(request,"signup.html",{"messg":message})
    uid = user['localId']
    
    data={"name":name, "email":email}

    database.child("users").child(uid).child("details").set(data)
    return render(request,"signIn.html")

