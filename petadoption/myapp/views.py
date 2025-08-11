from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from myapp.models import Booking, Category, PetType, Address, Pet
# Create your views here.

def pet_login(req):
    
    if 'user' in req.session:
        return redirect(home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        print(password,uname)
        shop=authenticate(username=uname,password=password)
        print(shop)
        if shop:
            login(req,user=shop)
            req.session['user']=uname
            return redirect(home)
     
        else:
            messages.warning(req,'invalid username or password')
            return redirect(pet_login)
    else:
        return render(req,'login.html')
    
    
def pet_logout(req):
    logout(req)
    req.session.flush()        
    return redirect(pet_login)



def register(req):
    if req.method == 'POST':
        uname = req.POST['uname']
        email = req.POST['email']
        pswd = req.POST['pswd']
        try:
            data = User.objects.create_user(first_name=uname, email=email, username=uname, password=pswd)
            data.save()
            shop=authenticate(username=uname,password=pswd)
            if shop:
                login(req,user=shop)
                req.session['user']=uname
                return redirect(home)
        
        except:
            messages.warning(req, 'user invalid')
            return redirect(register)
    else:
        return render(req, 'register.html')
    
    
@login_required
def home(request):

    if 'user' in request.session:
        try:

            categories = Category.objects.all()
        except:
            messages.warning(request, 'no categories')
        user = User.objects.get(username=request.session['user'])
        return render(request, 'home.html', {'categories': categories})

    else:

        return redirect(pet_login)
    
@login_required
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    pets = Pet.objects.filter(user=user)

    return render(request, 'user_profile.html', {'user': user, 'pets': pets})
    
@login_required
def add_pet(request):
    categories = Category.objects.all()
    pet_types = PetType.objects.all()
    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        pet_name = request.POST.get('pet_name')
        pet_description = request.POST.get('pet_description')
        pet_age = request.POST.get('pet_age')
        pet_price = request.POST.get('pet_price')
        pet_breed = request.POST.get('pet_breed')
        category_id = request.POST.get('category')
        pet_type_id = request.POST.get('pet_type')
        pet_image = request.FILES.get('pet_image')  

        category = Category.objects.get(id=category_id)
        pet_type = PetType.objects.get(id=pet_type_id)

        address_id = request.POST.get('address') 
        selected_address = Address.objects.get(id=address_id) if address_id else None

        
        pet = Pet(
            pet_name=pet_name,
            pet_description=pet_description,
            pet_age=pet_age,
            pet_price=pet_price,
            pet_breed=pet_breed,
            category=category,
            pet_type=pet_type,
            pet_image=pet_image,
            user=request.user, 
            address=selected_address  
        )
        pet.save()

        return redirect('pet_list')  

    return render(request, 'add_pets.html', {
        'categories': categories,
        'pet_types': pet_types,
        'addresses': addresses  
    })

# def add_pet_type(request):
#     if request.method == 'POST':
#         pet_type_name = request.POST.get('name')
        
#         pet_type = PetType(name=pet_type_name)
#         pet_type.save()
        
#         messages.success(request, 'Pet type added successfully!')
#         return redirect('add_pet_type')  

#     return render(request, 'add_pet_type.html')


def add_address(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        building_no = request.POST.get('building_no')
        street = request.POST.get('street')
        state = request.POST.get('state')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')
        mobile_no = request.POST.get('mobile_no')

        if len(mobile_no) != 10 or not mobile_no.isdigit():
            messages.warning(request, "Please enter a valid 10-digit mobile number.")
            return redirect('add_address')
        
        if len(str(pincode)) != 6 or not str(pincode).isdigit():
            messages.warning(request, "Please enter a valid 6-digit pincode.")
            return redirect('add_address')
        
        address = Address(
            user=request.user,
            name=name,
            building_no=building_no,
            street=street,
            state=state,
            district=district,
            pincode=pincode,
            mobile_no=mobile_no
        )
        address.save()
        messages.success(request, "Address added successfully!")
        return redirect('home')  

    return render(request, 'add_address.html',{'categories': categories})


# def add_category(request):
#     if request.method == 'POST':
#         category_name = request.POST.get('name')
#         image = request.FILES.get('image')  
#         category = Category(name=category_name,pet_image=image)
#         category.save()
#         print(image)
        
#         messages.success(request, 'Category added successfully!')
#         return redirect('add_category')  

#     return render(request, 'add_category.html')

@login_required
def view_address(request):
    categories = Category.objects.all()
    addresses = Address.objects.filter(user=request.user)  
    return render(request, 'view_address.html', {'addresses': addresses,'categories': categories})

@login_required
def view_pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    address = pet.address 
    return render(request, 'view_pet_details.html', {'pet': pet, 'address': address})

@login_required
def pet_list(request):
    categories = Category.objects.all()
    pets = Pet.objects.all()[::-1]
    return render(request, 'pet_list.html', {'pets': pets,'categories': categories})

@login_required
def delete_pet(request, id):
    pet = get_object_or_404(Pet, id=id)

    if pet.user != request.user:  
        messages.warning(request, "You are not authorized to delete this pet.")
        return redirect('pet_list')  

    if request.method == 'POST':
        pet.delete()
        messages.success(request, "Pet deleted successfully.")
        return redirect('pet_list')

    return render(request, 'confirm_delete.html', {'pet': pet})



@login_required
def view_address(request):
    categories = Category.objects.all()
    addresses = Address.objects.filter(user=request.user)  
    return render(request, 'view_address.html', {'addresses': addresses,'categories': categories})


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        address.delete()
        messages.success(request, "Address deleted successfully.")
        return redirect('view_address')

    return render(request, 'address_delete.html', {'address': address})


@login_required
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if pet.user != request.user:  
        messages.warning(request, "You are not authorized to edit this pet.")
        return redirect('pet_list')  

    categories = Category.objects.all()
    pet_types = PetType.objects.all()

    if request.method == 'POST':
        pet_name = request.POST.get('pet_name')
        pet_description = request.POST.get('pet_description')
        pet_age = request.POST.get('pet_age')
        pet_price = request.POST.get('pet_price')
        pet_breed = request.POST.get('pet_breed')
        category_id = request.POST.get('category')
        pet_type_id = request.POST.get('pet_type')
        pet_image = request.FILES.get('pet_image')

        if not pet_name or not pet_description or not pet_age or not pet_price or not pet_breed:
            messages.error(request, "All fields are required.")
            return render(request, 'edit_pet.html', {
                'pet': pet,
                'categories': categories,
                'pet_types': pet_types
            })

        try:
            pet_age = int(pet_age)
            pet_price = int(pet_price)
        except ValueError:
            messages.error(request, "Age and price must be numbers.")
            return render(request, 'edit_pet.html', {
                'pet': pet,
                'categories': categories,
                'pet_types': pet_types
            })

        try:
            category = Category.objects.get(id=category_id)
            pet_type = PetType.objects.get(id=pet_type_id)
        except Category.DoesNotExist:
            messages.error(request, "Invalid category.")
            return render(request, 'edit_pet.html', {
                'pet': pet,
                'categories': categories,
                'pet_types': pet_types
            })
        except PetType.DoesNotExist:
            messages.error(request, "Invalid pet type.")
            return render(request, 'edit_pet.html', {
                'pet': pet,
                'categories': categories,
                'pet_types': pet_types
            })

        pet.pet_name = pet_name
        pet.pet_description = pet_description
        pet.pet_age = pet_age
        pet.pet_price = pet_price
        pet.pet_breed = pet_breed
        pet.category = category
        pet.pet_type = pet_type

        if pet_image:  
            pet.pet_image = pet_image
        pet.save()

        messages.success(request, "Pet updated successfully.")
        return redirect('pet_list')

    return render(request, 'edit_pet.html', {
        'pet': pet,
        'categories': categories,
        'pet_types': pet_types
    })

@login_required
def pets_by_category(request, category_id ):
    categories = Category.objects.all()
    pets = Pet.objects.filter(category_id=category_id) 
    try:
        categories = Category.objects.all()
        pets = Pet.objects.filter(category_id=category_id)
        category = Category.objects.get(id=category_id) 
    except:
        messages.error(request, "Invalid category.")
        return render(request, 'pets_cat.html')

    return render(request, 'pets_cat.html', {'pets': pets, 'category': category,'categories': categories})


@login_required
def pet_detail(request, pet_id):
    categories = Category.objects.all()
    pet = get_object_or_404(Pet, id=pet_id)
    user = request.user
    address = pet.address 
    return render(request, 'pet_detail.html', {'pet': pet, 'address': address, 'user': user,'categories': categories})


@login_required
def book_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    amount_to_pay = pet.pet_price * 0.20
    
    try:
        user = get_object_or_404(Address,user=request.user)
    except:
        return redirect('add_address')

    if request.method == 'POST':
        booking = Booking.objects.create(
            pet=pet,
            user=request.user,
            payment_status=True,
            address = user,
            amount_paid=0
            )
        pet.is_available = False
        pet.save()

        messages.success(request, f"Your booking for the pet '{pet.pet_name}' was successful! Enjoy your adoption.")
        return render(request, 'booking_success.html', {'is_free_adoption': True, 'pet_name': pet.pet_name})
    return render(request, 'book_pet.html', {'pet': pet, 'amount_to_pay': amount_to_pay})
        
        

        

    # if request.method == 'POST':
    #     booking = Booking.objects.create(
    #         pet=pet,
    #         user=request.user,
    #         payment_status=False,
    #         amount_paid=amount_to_pay
    #     )

    #     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    #     razorpay_order = client.order.create(
    #         {"amount": int(amount_to_pay) * 100, "currency": "INR", "payment_capture": "1"}
    #     )
    #     order_id = razorpay_order['id']

    #     order = Order.objects.create(
    #         name=request.user.first_name,
    #         amount=amount_to_pay,
    #         provider_order_id=order_id,
    #         pet=pet,
    #         user=request.user
    #     )
    #     order.save()

    #     messages.success(request, "Booking successful! Please proceed with the payment.")
    #     return render(
    #         request,
    #         "user/payment.html",
    #         {
    #             "callback_url": "http://127.0.0.1:8000/callback",
    #             "razorpay_key": settings.RAZORPAY_KEY_ID,
    #             "order": order,
    #         },
    #     )
        

    
    
@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    categories = Category.objects.all()
    return render(request, 'view_bookings.html', {'bookings': bookings, 'categories':categories})

@login_required
def booking_success(request):
    return render(request, 'booking_success.html')