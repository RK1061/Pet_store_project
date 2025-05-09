from django.shortcuts import render,redirect
from petstoreapp.models import Pet, Cart, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
import razorpay
import uuid
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def index(request):
    user=request.user
    print("user logged in",user.is_authenticated)
    context={}
    allPets = Pet.objects.all()
    context ['pets']=allPets

    query = request.GET.get('q', '')
    if query:
        pets = Pet.objects.filter(Q(name__icontains=query)|Q(breed__icontains=query)|Q(type__icontains=query)|Q(price__icontains=query))
    else:
        pets = Pet.objects.all()
    return render(request, 'index.html', {'pets': pets, 'query': query})

def userlogin(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        # 1 fetch form data

        n=request.POST['uname']
        p=request.POST['password']
        
        user=authenticate(username=n,password=p)
        # print("LOGIN user after authenticate",user)
        if user is not None:
            # Successfull login
            login(request,user)
            return redirect("/")
        else:
            context={}
            context['error']="please enter valid username & password"
            return render(request,'login.html',context)

def userlogout(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method=="GET":
        return render(request,'register.html')
    else:
        n=request.POST['uname']
        e=request.POST['email']
        p=request.POST['password']
        cp=request.POST['c_password']

        context={}

        if n=="" or e=="" or p=="" or cp=="":
            context['error']='All fields are compulsary'
            return render(request,'register.html',context)
        elif p!=cp:
            context['error']='password & confirm password must be same '
            return render(request,'register.html',context)
        else:
            # user=User.objects.create(username=n,email=e,password=p)
            user=User.objects.create(username=n,email=e)
            user.set_password(p) #password encryption
            user.save()
            return redirect('/login')
        
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Prevent saving if username is empty
        if not name:
            messages.error(request, "Name cannot be empty.")
            return render(request, 'edit_profile.html')

        user.username = name  # 'username' is required by default User model
        user.email = email

        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)  # Prevents logout on password change

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('/editprofile')
    return render(request, 'Edit_profile.html')

def contactus(request):
    return render(request,'contactus.html')

def getPetById(request,petid):
    context = {}
    petObj = Pet.objects.get(id=petid)
    context['pets']=petObj
    return render(request,'details.html',context)

def filterByCategory(request,catName):
    context={}
    allPets=Pet.objects.filter(type=catName)
    context['pets']=allPets
    return render(request,'index.html',context)

#order by low price to high or high to low
def sortByPrice(request,direction):
    # order_by('price')   #for asc
    # order_by('-price')  #for desc
    if direction=='asc':
        column='price'
    else:
        column='-price'
    context={}
    allPets=Pet.objects.order_by(column)
    context['pets']=allPets
    return render(request,'index.html',context)

# filter by range n to n
def filterByRange(request):
    min = request.GET['min']
    max = request.GET['max']

    c1 = Q(price__gte=min)
    c2 = Q(price__lte=max)
    pets=Pet.objects.filter(c1 & c2)
    context={}
    context['pets']=pets
    return render(request,'index.html',context)

def addToCart(request,petid):
    selectedPet = Pet.objects.get(id=petid)
    userid = request.user.id
    if userid is not None:
        loggedinUser = User.objects.get(id=userid)
        cart=Cart.objects.create(uid=loggedinUser,petid=selectedPet)
        cart.save()
        return redirect ('/')
    else:
        # context={'error':'Please Login first to add in cart'}    
        return redirect('/login')

def showMyCart(request):
    userid = request.user.id
    user=User.objects.get(id = userid)
    myCart=Cart.objects.filter(uid=user)
    context={'mycart':myCart}
    print(myCart)
    count=len(myCart)
    TotalBill=0
    for cart in myCart:
        TotalBill+=cart.petid.price * cart.quantity
    context['count']=count
    context['Totalbill']=TotalBill
    return render(request,'mycart.html',context)

def removeCart(request,cartid):
    c = Cart.objects.filter(id=cartid)
    c.delete()
    return redirect('/mycart')

def updateQuantity(request,cartid,operation):
    ucart=Cart.objects.filter(id=cartid)

    if operation =='incr':
        q=ucart[0].quantity
        ucart.update(quantity=q+1)
        return redirect('/mycart')
    else:
        q=ucart[0].quantity
        ucart.update(quantity=q-1)
        return redirect('/mycart')
    
def confirmOrder(request):
    userid = request.user.id
    user=User.objects.get(id = userid)
    myCart=Cart.objects.filter(uid=user)
    context={'mycart':myCart}
    print(myCart)
    count=len(myCart)
    TotalBill=0
    for cart in myCart:
        TotalBill+=cart.petid.price * cart.quantity
    context['count']=count
    context['Totalbill']=TotalBill
    return render(request,'confirmorder.html',context)

def makepayment(request):
    userid = request.user.id
    data=Cart.objects.filter(uid=userid)
    total=0
    for cart in data:
        total += cart.petid.price * cart.quantity
    client = razorpay.Client(auth=("rzp_test_rMwZicGe9ePAbb", "cTqU3gbw5rZFDf08pml4dLVd"))

    data = { "amount":total*100, "currency": "INR", "receipt": " " }
    payment = client.order.create(data=data) # Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
    print(payment)
    context={}
    context['data']=payment
    return render(request,'pay.html',context)

def placeOrder(request):
    ordid = uuid.uuid4()
    userid = request.user.id
    cartlist = Cart.objects.filter(uid = userid)
    for cart in cartlist:
        order = Order.objects.create(orderid = ordid, userid = cart.uid, petid = cart.petid, quantity = cart.quantity)
        order.save()
    cartlist.delete()
   
    msg = "Thank You for Shopping with Us! We truly appreciate your purchase and your trust in us. We hope you enjoy your order and look forward to serving you again soon! your order id is : " +str(ordid)
    send_mail(
        "Order Place Successfully !!",
        msg,
        "saurabhdhelar@gmail.com",
        [request.user.email],
        fail_silently=False,
    )   
    return redirect('/')


