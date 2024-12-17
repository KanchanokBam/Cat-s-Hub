from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from .forms import SignUpForm 


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request)
            return redirect('/')  
        else:
            messages.error(request, 'Error')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # เปลี่ยน 'next-page' เป็น URL ของหน้าหลังจากเข้าสู่ระบบ
            else:
                messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    else:
        form = AuthenticationForm()

    return render(request, 'signin.html', {'form': form})

def logout_view(request):
    logout(request)  # ฟังก์ชัน Logout จาก Django
    return redirect('signin')  # หลัง Logout ให้เปลี่ยนเส้นทางไปที่หน้า Login


@login_required(login_url='/signin/')
def page1(request):
    return render(request, 'home.html')

@login_required  
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})
