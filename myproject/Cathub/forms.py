from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Cat ,UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Provide a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class CatPostForm(forms.ModelForm):
    image = forms.ImageField(required=False)  # ฟิลด์สำหรับอัปโหลดรูปภาพ

    class Meta:
        model = Cat
        fields = ['name', 'age', 'breed', 'color', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2', 'placeholder': 'Name'}),
            'age': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2', 'placeholder': 'Age'}),
            'breed': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2', 'placeholder': 'Breed'}),
            'color': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2', 'placeholder': 'Color'}),
        }


class BirthDateForm(forms.Form):
    day = forms.IntegerField(
        label="Day", min_value=1, max_value=31, 
        widget=forms.NumberInput(attrs={'placeholder': 'Day', 'class': 'border rounded px-3 py-2 w-full'})
    )
    month = forms.IntegerField(
        label="Month", min_value=1, max_value=12, 
        widget=forms.NumberInput(attrs={'placeholder': 'Month', 'class': 'border rounded px-3 py-2 w-full'})
    )
    year = forms.IntegerField(
        label="Year", min_value=1900, max_value=2024, 
        widget=forms.NumberInput(attrs={'placeholder': 'Year', 'class': 'border rounded px-3 py-2 w-full'})
    )


class ProfilePictureUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)  # รองรับการอัปโหลดไฟล์ภาพ

    class Meta:
        model = UserProfile
        fields = []  # ไม่ต้องระบุ fields อื่น เพราะจะจัดการผ่าน Base64