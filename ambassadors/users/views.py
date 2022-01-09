from django.core.checks import messages
from django.shortcuts import render
from django.shortcuts import redirect, render
from .models import Account
from .forms import LoginForm, RegistrationForm, UserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model


User = get_user_model()


def signup_view(request):
    
    # Get referral user id
    profile_id = request.session.get('ref_profile')
    print("Referral ID: ", profile_id)
    
    # Get user by the referral user id
    recommended_by_profile = Account.objects.get(id=profile_id)
    print("Recommended By Profile: ", recommended_by_profile.fullname())
    
    # User Profile and Account form creation
    userform = UserForm()
    form = RegistrationForm()
    
    if request.method == 'POST':
        userform = UserForm(request.POST or None)
        form = RegistrationForm(request.POST or None)
        
        if userform.is_valid() and form.is_valid():
            print('is valid', userform.is_valid())
            
            if profile_id is not None:
                
                # Gets cleaned data from user form
                email = userform.cleaned_data.get("email")
                password = userform.cleaned_data.get("password")
                confirm_password = userform.cleaned_data.get("confirm_password")
                
                # Checks if password equals to confirm password
                password = True if password == confirm_password else False
                
                # If it does, run the next block of code
                if password is True:
                    
                    # Create user
                    user = User.objects.create(
                        email=email,
                        password=confirm_password
                    )
                    
                    # Set user password
                    user.password = user.set_password(confirm_password)
                    
                else:
                    
                    # If it doesn't, redirect the user back to the sign up page
                    # with an error message telling them that their password
                    # does not match and should try again!
                    messages.error(request, "Password does not match. Try again!")
                    return redirect("users:signup")
                
                
                # Gets user with the instance --> email
                registered_user = User.objects.get(email=email)
                print("Registered User: ", registered_user)
                
                # Saves form
                user_account = form.save(commit=False)
                
                # Adds user id to user account id
                user_account.user = registered_user
                
                # Saves user_account to database
                user_account.save()
                
                # Gets the registered user of the user account
                registered_profile = Account.objects.get(user=registered_user)
                print('Registered Profile: ', registered_profile)
                
                # Adds whoever recommended that user to his/her recommended_by
                registered_profile.recommended_by = recommended_by_profile.user
                
                # Saves registered profile to database
                registered_profile.save()
                
                # Redirects user to the login page
                return redirect("users:sign-in")
                
            else:
                userform.save()
                form.save()
                email = userform.cleaned_data.get('email')
                password = userform.cleaned_data.get('password')
                user = authenticate(email=email, password=password)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('main-view')
            
    context = {
        'form': form, 
        'userform': userform,
        'recommended_by_profile': recommended_by_profile
    }
    print("Recommended By Profile: ", recommended_by_profile.fullname())
    return render(request, 'page/signup.html', context)


def login_page(request):
    
    # Login form
    form = LoginForm()
        
    if request.method == "POST":
        
        # Login form with POST request
        form = LoginForm(request.POST)
        print("Is Form Valid: ", form.is_valid())
        
        # Check if form is valid
        if form.is_valid():
        
            # Get email and password from form POST request
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            
            print("Email: ", email)
            print("Password: ", password)
            
            # Get user with the above email
            user = User.objects.get(email=email)
            
            # Authenticates user with the above credentials
            user = authenticate(
                request, username=user.email, password=user.password
            )
            print("User: ", user)
            
            # Checks if the user exists
            if user is not None:
                
                # Logs the user in
                login(request, user)
                
                # Redirecct user to the dashboard page
                redirect("users:recommendations")
            
            # If the user doesn't exist
            else:
                
                print("User doesn't exist!")
                # Redirects user back to the login page
                redirect("users:sign-in")
    context = {
        "form": form
    }
    return render(request, "page/login.html", context)


def main_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    
    try:
        profile = Account.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id', profile.id)
    except:
        pass
    
    print(request.session.get_expiry_date())
    return render(request, 'page/profile.html', {})


def dashboard(request):
    # 
    referrals = Account.objects.get(user=request.user)
    my_recs = referrals.get_recommended_profiles()
    count = len(my_recs)
    ref_percentage = 0.0
    
    for stake in my_recs:
        ref_amt = stake.amt_staked
        ref_percentage = ref_amt * 2/100

    # 
    downline_percentage = (count/1000) * 100
    amount = referrals.usd_pooled
    points = amount / 200000
    points_percentage = points / 6000 * 100
    
    # Dashboard context
    context = {
        'my_recs': my_recs, 
        'referrals': referrals,
        'count': count, 
        'downline_percentage': downline_percentage,
        'points': points, 
        'points_percentage': points_percentage, 
        'ref_percentage': ref_percentage
    }
    return render(request, 'page/dashboard.html', context)
