from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialApp
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from home.forms import CustomAuthenticationForm
from django.urls import reverse
from allauth.account.views import SignupView



# Create your views here.
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect("/")

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))  # Replace with your success redirect URL
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomAuthenticationForm()

    context = {'form': form}
    return render(request, 'registration/login.html', context)


# class CustomSignupView(SignupView):
#     # Customize signup view as needed
#     form_class = SignupView
#     template_name = 'account/signup.html'  # Specify custom template
#     success_url = 'account/login/'


