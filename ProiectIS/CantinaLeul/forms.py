from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

#formularul specific creari unui utilizator nou
class newUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model=User
        fields=('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

#formularul specific creari unui produs nou din meniu
class newProductForm(forms.ModelForm):
    class Meta:
        model=newProduct
        exclude=['bucatar']

#formularul specific creari unui utilizator nou pentru editare
class myUserForm(forms.ModelForm):
    class Meta:
        model=newUser
        exclude=['user', 'nr_matricol', 'facultate', 'reducere', 'abonament', 'tip', 'data_expirare', 'cerere_abonament']

#formularul specific editarii datelor unui bucatar
class myChefForm(forms.ModelForm):
    class Meta:
        model=newChef
        exclude=['user', 'imagine']

#formularul specific editarii datelor privind parola(resetarea parolei)
class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)