from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy
from django.contrib.admin import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Item, Code


class AddItemForm(forms.ModelForm):
    
    def clean_item_count(self):
        item_count = self.cleaned_data['item_count']
        if item_count <= 0:
            raise ValidationError('The count must be more than zero')
        return item_count

    class Meta:
        model = Item
        fields = ("item_type", "item_name", "item_count", "item_counttype", 
                    "item_description", "item_executed", "item_isdone")
        labels= {
            'item_type': ugettext_lazy('Group'),
            'item_name': ugettext_lazy('Name'),
            'item_count': ugettext_lazy('Count'),
            'item_counttype': ugettext_lazy('Type of count'),
            'item_description': ugettext_lazy('Description'),
            'item_executed': ugettext_lazy('Need on'),
            'item_isdone' : ugettext_lazy('Is done'),
        }
        widgets = {
            'item_executed': forms.DateInput(attrs={'class': 'date-input', 
                                                    'autocomplete': 'off'}),
        }


class SignUpInitForm(forms.ModelForm):
    email = forms.EmailField(label='Registration email', max_length=254, 
                                help_text='Enter your email') 

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('You have an account yet')
        return email

    class Meta:
        model = User
        fields = ('email', )


class SignUpCheckForm(forms.ModelForm):
    code_value = forms.CharField(label='Registration code', max_length=8, 
                                    help_text='Enter your code')

    def clean_code_value(self):
        user_code = self.cleaned_data['code_value']
        if Code.objects.filter(code_value=user_code).exists():
            return user_code
        else:
            raise ValidationError('Incorrect code. You have only 5 attempts!')

    class Meta:
        model = Code
        fields = ('code_value', )


class SignUpForm(UserCreationForm): 

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )


class ResetPassInitForm(forms.ModelForm):
    email = forms.EmailField(label='Email of your account', max_length=254, 
                                help_text='Enter your email') 

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError('Email does not exists')
        return email

    class Meta:
        model = User
        fields = ('email', )


class ResetPassCheckForm(forms.ModelForm):
    code_value = forms.CharField(label='Reset code', max_length=8, 
                                    help_text='Enter your code')

    def clean_code_value(self):
        user_code = self.cleaned_data['code_value']
        if Code.objects.filter(code_value=user_code).exists():
            return user_code
        else:
            raise ValidationError('Incorrect code. You have only 5 attempts!')

    class Meta:
        model = Code
        fields = ('code_value', )


class ResetPassChangeForm(forms.Form):
    new_password1 = forms.CharField(label='New password', 
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='New password confirmation', 
                                    widget=forms.PasswordInput)
    
    def clean_new_password2(self):
        password1 = self.cleaned_data['new_password1']
        password2 = self.cleaned_data['new_password2']
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('The two password fields \
                                                did not match')
        return password2
