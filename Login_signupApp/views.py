from django.shortcuts import render,redirect
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        if request.method =='POST':
            if 'signup' in request.POST['action']:
                print(request.POST)
                saved_successfully = False
                user_already_exists = False
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                email=request.POST['email']
                password = request.POST['password']
                #regno=request.POST['regno']
                # Instantiate a Register object with the extracted field values
                
                
                # Save the Register object to the database
                try:
                    # Try to save the Register object
                    User.objects.create_user(username=email,first_name=firstname,last_name=lastname, email=email, password=password)
                    saved_successfully = True
                except IntegrityError:
                    # If IntegrityError is raised (due to non-unique email or regno), set user_already_exists to True
                    user_already_exists = True
                
                return render(request, 'html/login_signup.html',{'saved_successfully': saved_successfully, 'user_already_exists': user_already_exists})
            else:
            
                print(request.POST)
                # Handling login
                log_email = request.POST['email']
                print(log_email)
                log_password = request.POST['password']
                print(log_password)
                # Check if a user with the given email and password exists
                
                user = authenticate(request, username=log_email, password=log_password)
                
                if user is not None:
                    login(request, user)
                    
                    return redirect('dashboard')  # Redirect to dashboard after successful login
                else:
                    return render(request, 'html/login_signup.html', {'login_failed': True})
                
        else:
            return render(request, 'html/login_signup.html',{})

def forgetpass_view(request):
    if request.method == 'POST':
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        
        
        # Check if a user with the provided email exists
        try:
            register = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'html/forgetpass.html', {'error_message': 'User does not exist'})
        
        # Check if the passwords match
        if password != confirm_password:
            return render(request, 'html/forgetpass.html', {'error_message': 'Passwords do not match'})

        # Update the user's password
        register.password = password
        register.save()

        # Optionally, you can redirect the user to a success page
        return render(request, 'html/login_signup.html',{'reset_pass':True})
    else:
        return render(request, 'html/forgetpass.html', {})

def dashboard(request):
    if request.user.is_authenticated:
        # Access session variables
        user_email = request.user.email
        user_id = request.user.id
        return render(request, 'html/dashboard.html', {'user_email': user_email, 'user_id': user_id})
    else:
        return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/')

def profile_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user

            # Handle profile image upload
            profile_image = request.FILES.get('profile_image')
            if profile_image:
                # Get or create the user's profile
                profile, created = UserProfile.objects.get_or_create(user=user)
                # Update the profile image
                profile.profile_image = profile_image
                profile.save()

            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')

            # Update user data
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.username = email
            user.save()

            # Retrieve the profile image if it exists
            profile = UserProfile.objects.filter(user=user).first()
            profile_image=None
            if profile:
                profile_image = profile.profile_image

            context = {'user': user, 'profile_image': profile_image}

            messages.success(request, 'Profile updated successfully.')
            return render(request, 'html/profile.html',context)
            
        else:
            user = request.user
            profile = UserProfile.objects.filter(user=user).first()
            profile_image=None
            if profile:
                profile_image = profile.profile_image

            context = {'user': user, 'profile_image': profile_image}
            return render(request, 'html/profile.html',context)
    else:
        return redirect('/')
    
