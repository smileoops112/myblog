from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth import authenticate


class SignUpForm(forms.Form):

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputUsername',
            'placeholder': 'Имя пользователя',
        }),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'inputPassword',
            'placeholder': 'Пароль'
        })
    )
    password_repeat = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'ReInputPassword',
            'placeholder': "Повтор пароля",
        })
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['password_repeat']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth


class SignInForm(forms.Form):

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-2',
            'id': 'inputUsername',
            'placeholder': 'Имя пользователя',
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'inputPassword',
            'placeholder': 'Пароль'
        })
    )


class FeedBackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'name',
            'placeholder': 'Ваше имя"'
            }
        )
    )
    email = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'Ваша почта'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'subject',
            'placeholder': 'Тема'
        })
    )
    message = forms.CharField(
        max_length=200,
        widget=forms.Textarea(attrs={
            'id': 'message',
            'class': 'form-class md-textarea',
            'placeholder': 'Ваше сообщение',
            'rows': 2
        })
    )
