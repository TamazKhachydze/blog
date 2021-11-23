from django import forms
from django.contrib.auth import get_user_model

from .models import Comment


User = get_user_model()


class LoginForm(forms.ModelForm):

    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f"Пользователь с логином {username} не найден")
        if not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password',)


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput())
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Имя', required=False)
    last_name = forms.CharField(label='Фамилия', required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name',)


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
        'placeholder': 'Ваш комментарий...'
    }))
    class Meta:
        model = Comment
        fields = ('text',)