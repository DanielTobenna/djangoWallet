from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class ContactForm(forms.Form):
	name= forms.CharField(max_length=150)
	email= forms.EmailField()
	message= forms.CharField(widget=forms.Textarea)

class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    class Meta:
        model = get_user_model()
        fields = ['email']

#class CreateUserForm(UserCreationForm):
	#email = forms.EmailField(required=True)
	#def clean_email(self):
		#if User.objects.filter(email=self.cleaned_data['email']).exists():
			#raise forms.ValidationError("The email is already registered")
		#return self.cleaned_data['email']
	#class Meta:
		#model = User
		#fields = ['username','email', 'password1', 'password2']


class CustomerForm(ModelForm):
	class Meta:
		model= Customer
		fields= '__all__'
		exclude= ['email', 'usdt', 'btc',
			'eth', 'dodge', 'trx', 'sol', 'ltc', 'dot', 'xlm', 'ada',
			'elm', 'pyn', 'rdn', 'ttm', 'axs', 'floki', 'busd', 'dash', 'etc',
			'xmr', 'bnbbsc', 'shib', 'bch', 'xrp'

		]












