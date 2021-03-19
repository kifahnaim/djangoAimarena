from authapp import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input100', 'type': 'text', 'name': 'username', 'placeholder': 'Type your username'}))
    password = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input100', 'type': 'password', 'name': 'password', 'placeholder': 'Type your password'}))