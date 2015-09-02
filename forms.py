from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from django.core import validators
from .models import Comments


class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()


class MyRegForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Пароли не совпадают!",
    }
    password1 = forms.CharField(min_length=6, label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=6, label='Введите пароль еще раз',
                                help_text="Введите повторно пароль для проверки",
                                widget=forms.PasswordInput)
    last_name = forms.CharField(max_length=50, label='Фамилия')
    first_name = forms.CharField(max_length=50, label='Имя')
    phone = forms.CharField(max_length=30, label='Телефон',
                            help_text='Телефон в формате ***-*******',
                            validators=[
                                validators.RegexValidator(r'^\d{3}\-\d{7}$',
                                                          'Введите телефон в правильном формате!(***-*******)',
                                                          'invalid'), ])
    date_of_birth = forms.DateField(label='Дата рождения', required=True, widget=SelectDateWidget(empty_label="Nothing"))

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username', 'email', 'password1', 'password2', 'date_of_birth', 'phone')

    def save(self, commit=True):
        user = super(MyRegForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class AvatarForm(forms.Form):
    avatar = forms.ImageField(label='Загрузить аватар')
    bl_wh = forms.BooleanField(label='Сделать черно-белым', required=False)


class EditProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(label='Дата рождения', required=True,
                                    widget=SelectDateWidget(empty_label="Nothing"))
    phone = forms.CharField(max_length=30, label='Телефон',
                            help_text='Телефон в формате ***-*******',
                            validators=[
                                validators.RegexValidator(r'^\d{3}\-\d{7}$',
                                                          'Введите телефон в правильном формате!(***-*******)',
                                                          'invalid'), ])

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username', 'email', 'date_of_birth', 'phone', )
        exclude = ('password',)


class AddCommentForm(forms.ModelForm):
    message = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'cols': 20, 'rows': 5}))

    class Meta:
        model = Comments
        fields = ('message',)