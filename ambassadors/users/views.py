from django.shortcuts import render

from django.shortcuts import redirect, render
from .models import Account
from .forms import RegistrationForm, UserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


def signup_view(request):
    profile_id = request.session.get('ref_profile')
    print('profile_id', profile_id)
    if request.method == 'POST':
        userform = UserForm(request.POST or None)
        form = RegistrationForm(request.POST or None)
        if userform.is_valid() and form.is_valid():
            print('is valid', userform.is_valid())
            if profile_id is not None:
                recommended_by_profile = Account.objects.get(id=profile_id)

                userform.save()
                instance = userform.save()
                # form.save()
                registered_user = User.objects.get(id=instance.id)
                registered_profile = Account.objects.get(user=registered_user)
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()
            else:
                userform.save()
                form.save()
                email = userform.cleaned_data.get('email')
                password = userform.cleaned_data.get('password')
                user = authenticate(email=email, password=password)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('main-view')
    else:
        userform = UserForm()
        form = RegistrationForm()
        context = {'form': form, 'userform': userform}
        return render(request, 'page/signup.html', context)

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
    referrals = Account.objects.get(user=request.user)
    my_recs = referrals.get_recommended_profiles()
    count = len(my_recs)
    ref_percentage = 0.0
    for stake in my_recs:
        ref_amt = stake.amt_staked
        ref_percentage = ref_amt * 2/100
    # Calculate the percent of AMT, USD Pooled and points gathered for users
    downline_percentage = (count/1000) * 100
    amount = referrals.usd_pooled
    points = int(amount/33.33)
    points_percentage = int(points/6000 * 100)
    context = {'my_recs': my_recs, 'referrals': referrals,
               'count': count, 'downline_percentage': downline_percentage,
               'points': points, 'points_percentage': points_percentage, 'ref_percentage': ref_percentage}
    return render(request, 'page/dashboard.html', context)
