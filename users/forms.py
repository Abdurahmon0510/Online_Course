from django import forms

from course.models import Course
from users.field import MultiEmailField
from .models import User
from .models import Teacher


class TeacherModelForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'phone', 'image', 'slug']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput())
    username = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This {email} is already exists')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

    def save(self, commit=True):
        try:
            user = super(RegisterForm, self).save(commit=False)
            user.set_password(self.cleaned_data['password'])
            user.is_active = False
            user.is_superuser = False
            user.is_staff = False

            if commit:
                user.save()

            return user
        except Exception as e:
            raise forms.ValidationError(f'An error occurred while saving the user: {str(e)}')




class SendingEmailForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)
    recipient_list = MultiEmailField(widget=forms.Textarea)

class SignupForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Select a course")