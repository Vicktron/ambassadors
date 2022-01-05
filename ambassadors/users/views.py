from django.shortcuts import render

from django.shortcuts import redirect, render
from .models import Account
from .forms import RegistrationForm, UserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


def signup_view(request):
    profile_id = request.session.get('ref_profile')
    print('profile_id', profile_id)
    userform = UserForm(request.POST or None)
    form = RegistrationForm(request.POST or None)
    if userform.is_valid() and form.is_valid():
        if profile_id is not None:
            recommended_by_profile = Account.objects.get(id=profile_id)

            instance = form.save()
            registered_user = User.objects.get(id=instance.id)
            registered_profile = Account.objects.get(user=registered_user)
            registered_profile.recommended_by = recommended_by_profile.user
            registered_profile.save()
        else:
            form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        login(request, user)
        return redirect('main-view')

    context = {'form': form, 'userform': userform}
    return render(request, 'dist/signup.html', context)


def main_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Account.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id', profile.id)
    except:
        pass
    print(request.session.get_expiry_date())
    return render(request, 'dist/profile.html', {})


def dashboard(request):
    referrals = Account.objects.get(user=request.user)
    my_recs = referrals.get_recommended_profiles()
    context = {'my_recs': my_recs}
    return render(request, 'dist/dashboard.html', context)
