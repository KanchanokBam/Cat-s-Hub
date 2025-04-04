from django import forms
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Cat ,UserProfile,FeaturedProject

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
    image = forms.ImageField(required=False)

    AGE_CHOICES = [
        ('kitten', 'แมวเด็ก'),
        ('adult', 'แมวโต'),
        ('senior', 'แมวอายุมาก'),
    ]
    
    age_group = forms.ChoiceField(
        choices=AGE_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2'}),
        required=True,
        label="ช่วงอายุ"
    )

    PERSONALITY_CHOICES = [
        ('ขี้เล่น', 'ขี้เล่น'),
        ('รักเจ้าของ', 'รักเจ้าของ'),
        ('อยากรู้อยากเห็น', 'อยากรู้อยากเห็น'),
        ('ขี้เกียจ', 'ขี้เกียจ'),
        ('อ่อนโยน ', 'อ่อนโยน'),
        ('กล้าหาญ', 'กล้าหาญ'),
        ('ฉลาด', 'ฉลาด'),
        ('เป็นมิตร', 'เป็นมิตร'),
        ('เป็นตัวของตัวเอง', 'เป็นตัวของตัวเอง'),
        ('สบายๆ', 'สบายๆ'),
        ('กระตือรือร้น', 'กระตือรือร้น'),
        ('ชอบอิสระ', 'ชอบอิสระ'),
        
    ]
    
    personality = forms.ChoiceField(
        choices=PERSONALITY_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2'}),  
        required=True,
        label="Personality"
    )

    class Meta:
        model = Cat
        fields = ['name', 'age_group', 'breed', 'color', 'personality', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2', 'placeholder': 'Name'}),
            'breed': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2', 'placeholder': 'Breed'}),
            'color': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-4 py-2', 'placeholder': 'Color'}),
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
        fields = []  # ไม่ต้องระบุ fields อื่น เพราะจะจัดการผ่าน ImageField




class CatForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Cat
        fields = ['name', 'age_group', 'breed', 'color', 'personality', 'image']  # เปลี่ยนจาก 'age' เป็น 'age_group'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'age_group': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
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

class FeaturedProjectForm(forms.ModelForm):
    class Meta:
        model = FeaturedProject
        fields = ['title', 'description', 'url', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'description': forms.Textarea(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'url': forms.URLInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'image': forms.FileInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
        }
