from django import forms
from datetime import datetime
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
    
    # เพิ่มคำว่า "กรุณาเลือก" เป็น default option
    PERSONALITY_CHOICES = [
        ('', 'กรุณาเลือก'),  # ตัวเลือกแรกที่แสดง "กรุณาเลือก" (ค่าจะเป็น empty string)
        ('playful', 'Playful'),
        ('calm', 'Calm'),
        ('friendly', 'Friendly'),
        ('independent', 'Independent'),
        ('curious', 'Curious'),
    ]
    
    personality = forms.ChoiceField(
        choices=PERSONALITY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded px-4 py-2'
        }),
        required=False,  # ไม่บังคับให้เลือก
        label="Personality"
    )

    class Meta:
        model = Cat
        fields = ['name', 'age', 'breed', 'color', 'personality', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2', 
                'placeholder': 'Name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2', 
                'placeholder': 'Age'
            }),
            'breed': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2', 
                'placeholder': 'Breed'
            }),
            'color': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2', 
                'placeholder': 'Color'
            }),
        }


class BirthDateForm(forms.Form):
    birth_date = forms.DateField(
        label="Birth Date",
        widget=forms.DateInput(
            attrs={
                'type': 'date',  # HTML5 Date Picker
                'class': 'border rounded px-3 py-2 w-full',  # ใช้ TailwindCSS สำหรับ styling
            }
        )
    )



class ProfilePictureUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)  # รองรับการอัปโหลดไฟล์ภาพ

    class Meta:
        model = UserProfile
        fields = []  # ไม่ต้องระบุ fields อื่น เพราะจะจัดการผ่าน Base64


class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ['name', 'age', 'breed', 'color', 'personality', 'image_base64']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'age': forms.NumberInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'breed': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'color': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'personality': forms.Textarea(attrs={'class': 'border rounded px-3 py-2 w-full'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }