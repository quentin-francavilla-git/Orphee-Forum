""""
Defines form of the website.
"""
from cProfile import label
from email import message
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.Form):
    pseudo = forms.CharField(label = "", max_length = 200,
        widget=forms.TextInput(attrs={'placeholder' : 'Pseudonyme', 'class': 'regular_input'}))

    email = forms.EmailField(label = "", max_length = 200,
        widget=forms.TextInput
        (attrs={'placeholder' : 'Email', 'class': 'regular_input'}),
        error_messages={
        'required': 'Merci d\'insérer votre adresse mail.'})

    password = forms.CharField(label = "",
        widget = forms.PasswordInput
        (attrs={'placeholder' : 'Mot de passe', 'class': 'regular_input'}))

    passwordConfirmation = forms.CharField(label = "",
        widget = forms.PasswordInput
        (attrs={'placeholder' : 'Confirmation', 'class': 'regular_input'}))

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label = "", max_length = 200,
        widget=forms.TextInput
        (attrs={'placeholder' : 'Pseudonyme', 'class': 'regular_input'}))

    password = forms.CharField(label = "",
        widget = forms.PasswordInput
        (attrs={'placeholder' : 'Mot de passe', 'class': 'regular_input'}))

class DeleteForm(forms.Form):
    password = forms.CharField(label = "",
        widget = forms.PasswordInput
        (attrs={'placeholder' : 'Mot de passe', 'class': 'regular_input'}))

class TopicForm(forms.Form):
    anonymous = forms.BooleanField(required=False, label="Cochez pour publier le message anonymement")
    title = forms.CharField(label = "", max_length = 200,
        widget=forms.TextInput(attrs={'placeholder' : 'Titre du topic', 'class': 'regular_input'}))
    message = forms.CharField(label = "", 
        widget=forms.Textarea(attrs={'placeholder' : 'Votre message...', 'class': 'regular_textarea', 'rows': 15, 'cols': 15}))

class MessageForm(forms.Form):
    message = forms.CharField(label = "", 
        widget=forms.Textarea(attrs={'placeholder' : 'Votre réponse...', 'class': 'regular_textarea', 'rows': 5, 'cols': 15}))

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label = "", max_length = 200,
        widget=forms.TextInput
        (attrs={'placeholder' : 'Email', 'class': 'regular_input'}),
        error_messages={
        'required': 'Merci d\'insérer votre adresse mail.'})

class ResetPasswordFormToken(forms.Form):
    token = forms.CharField(label = "", max_length = 200,
        widget=forms.TextInput
        (attrs={'placeholder' : 'Token', 'class': 'regular_input'}))

    password = forms.CharField(label = "",
        widget = forms.PasswordInput
        (attrs={'placeholder' : 'Nouveau mot de passe', 'class': 'regular_input'}))