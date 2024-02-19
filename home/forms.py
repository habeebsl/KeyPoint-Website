from django import forms
from .models import SavedData
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm


class EmphasisDataForm(forms.Form):
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder':'Write Something...', 'id':'specific-input'}))


class SaveDataForm(forms.ModelForm):
    class Meta:
        model = SavedData
        fields = ['title',]

        widgets={
            'title':forms.TextInput(attrs={'id':'title', 'placeholder':'Change Title'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = ''


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['username'].label = False
        self.fields['password'].label = False


class CustomSignupForm(SignupForm):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add attributes to the existing form fields
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        self.fields['username'].label = False
        self.fields['email'].label = False
        self.fields['password1'].label = False
        self.fields['password2'].label = False
        self.fields['password1'].help_text = ""


class ChangeUsername(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['username'].label = False

    class Meta:
        model = User
        fields = ['username',]

        widgets={
            'username':forms.TextInput(attrs={'placeholder':'Username'})
        }
