from django import forms
from .models import Order

from django.contrib.auth.models import User


class LoginForm(forms.Form):
	username = forms.CharField(widget = forms.EmailInput(attrs=
		{'name':"username",'id':"username",'required':'required','placeholder':"Email",'class':'form-control form-control-lg'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs=
		{'name':'password','id':'password','class':"logininput",'placeholder':'Password','class':'form-control form-control-lg'}))

class RegisterForm(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=
		{'name':'password','id':'password','placeholder':'Password','class':'form-control form-control-lg'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=
		{'name':'confirm-password','id':'confirm-password','placeholder':'Confirm Password','class':'form-control form-control-lg'}))
	username = forms.CharField(widget=forms.EmailInput(attrs=
		{'name':"username",'id':"name",'placeholder':"Email",'class':'form-control form-control-lg'}))
	class Meta:
		model = User
		fields = ['username','password1','password2']


CHOICES=[('Student Project','Student Project'),
         ('Sponsored Project','Sponsored Project'),
         ('Consultancy Project','Consultancy Project')]

class orderForm(forms.Form):
	name = forms.CharField(widget = forms.TextInput(attrs=
		{'name':"username",'id':"username",'required':'required','placeholder':"Name",'class':'form-control form-control-lg'}))
	mail = forms.CharField(widget = forms.EmailInput(attrs=
		{'name':'mail','id':'mail','required':'required','placeholder':"Email",'class':'form-control form-control-lg'}))
	mobile = forms.CharField(widget = forms.NumberInput(attrs=
		{'name':"mobile",'id':"mobile",'required':'required','placeholder':"Mobile",'class':'form-control form-control-lg'}))
	title = forms.CharField(widget = forms.TextInput(attrs=
		{'name':"title",'id':"title",'required':'required','placeholder':"Work order title",'class':'form-control form-control-lg'}))
	work = forms.CharField(required=False,widget = forms.Textarea(attrs=
		{'name':'work','id':'work','placeholder':"Work Description",'class':'form-control form-control-lg'}))
	worktype = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs=
    	{'name':"worktype",'id':"worktype",'class':'radio-inline'}))
	file = forms.FileField(required=False,widget = forms.FileInput(attrs=
		{'name':'file','id':'file','placeholder':'Upload your file','class':'form-control form-control-lg'}))
	prof_name = forms.CharField(widget = forms.TextInput(attrs=
		{'name':"prof_name",'id':"prof_name",'required':'required','placeholder':"Name of Guide/Incharge",'class':'form-control form-control-lg'}))
	prof_mail = forms.CharField(widget = forms.EmailInput(attrs=
		{'name':"prof_mail",'id':"prof_mail",'required':'required','placeholder':"Email of Guide/Incharge",'class':'form-control form-control-lg'}))
	class Meta:
		model = Order
		fields = ['name', 'mail','mobile','work','worktype','file','prof_name','prof_mail']
		

CHOICES1=[('Accept','Accept'),
		('Reject','Reject'),
		('May be','May be')]

CHOICES3 = [
    ('In Progress', 'In Progress'),
    ('Work Done', 'Work Done')]

class DecisionForm(forms.Form):
    decision = forms.ChoiceField(choices=CHOICES1, widget=forms.RadioSelect(attrs={
        'name': "result", 'id': "result", 'class': 'radio-inline'}))
    decision1 = forms.ChoiceField(choices=CHOICES3, widget=forms.RadioSelect(attrs={
        'name': "result1", 'id': "result1", 'class': 'radio-inline'}))
    remarks = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'name': 'remarks', 'id': 'remarks', 'placeholder': "Remarks", 'class': 'form-control form-control-lg'}))

CHOICES2=[('Yes','Yes'),
		('No','No')]

class StatusForm(forms.Form):
	status_input = forms.CharField(required=True,widget = forms.Textarea(attrs=
		{'name':'status_input','id':'status_input','placeholder':"Please enter the status here",'class':'form-control form-control-lg'}))
	completed_input = forms.ChoiceField(required=False,choices=CHOICES2, widget=forms.RadioSelect(attrs=
    	{'name':"completed_input",'id':"completed_input",'class':'radio-inline'}))

CHOICES=[('Student Project','Student Project'),
         ('Sponsored Project','Sponsored Project'),
         ('Consultancy Project','Consultancy Project')]

class orderForm(forms.Form):
	name = forms.CharField(widget = forms.TextInput(attrs=
		{'name':"username",'id':"username",'required':'required','placeholder':"Name",'class':'form-control form-control-lg'}))
	mail = forms.CharField(widget = forms.EmailInput(attrs=
		{'name':'mail','id':'mail','required':'required','placeholder':"Email",'class':'form-control form-control-lg'}))
	mobile = forms.CharField(widget = forms.NumberInput(attrs=
		{'name':"mobile",'id':"mobile",'required':'required','placeholder':"Mobile",'class':'form-control form-control-lg'}))
	title = forms.CharField(widget = forms.TextInput(attrs=
		{'name':"title",'id':"title",'required':'required','placeholder':"Work order title",'class':'form-control form-control-lg'}))
	work = forms.CharField(required=False,widget = forms.Textarea(attrs=
		{'name':'work','id':'work','placeholder':"Work Description",'class':'form-control form-control-lg'}))
	worktype = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs=
    	{'name':"worktype",'id':"worktype",'class':'radio-inline'}))
	file = forms.FileField(required=False,widget = forms.FileInput(attrs=
		{'name':'file','id':'file','placeholder':'Upload your file','class':'form-control form-control-lg'}))
	prof_name = forms.CharField(widget = forms.TextInput(attrs=
		{'name':"prof_name",'id':"prof_name",'required':'required','placeholder':"Name of Guide/Incharge",'class':'form-control form-control-lg'}))
	prof_mail = forms.CharField(widget = forms.EmailInput(attrs=
		{'name':"prof_mail",'id':"prof_mail",'required':'required','placeholder':"Email of Guide/Incharge",'class':'form-control form-control-lg'}))
	class Meta:
		model = Order
		fields = ['name', 'mail','mobile','work','worktype','file','prof_name','prof_mail']
		

CHOICES1=[('Accept','Accept'),
		('Reject','Reject'),
		('May be','May be')]

class DecisionForm(forms.Form):
	decision = forms.ChoiceField(choices=CHOICES1, widget=forms.RadioSelect(attrs=
    	{'name':"result",'id':"result",'class':'radio-inline'}))
	decision1 = forms.ChoiceField(choices=CHOICES3, widget=forms.RadioSelect(attrs={
        'name': "result1", 'id': "result1", 'class': 'radio-inline'}))
	remarks = forms.CharField(required=False,widget = forms.Textarea(attrs=
		{'name':'remarks','id':'remarks','placeholder':"Remarks",'class':'form-control form-control-lg'}))

CHOICES2=[('Yes','Yes'),
		('No','No')]

class StatusForm(forms.Form):
	status_input = forms.CharField(required=True,widget = forms.Textarea(attrs=
		{'name':'status_input','id':'status_input','placeholder':"Please enter the status here",'class':'form-control form-control-lg'}))
	completed_input = forms.ChoiceField(required=False,choices=CHOICES2, widget=forms.RadioSelect(attrs=
    	{'name':"completed_input",'id':"completed_input",'class':'radio-inline'}))

	
