from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Cat, User,UserProfile
from .forms import SignUpForm, CatPostForm, UsernameUpdateForm, BirthDateForm ,ProfilePictureUpdateForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ทำการล็อกอินผู้ใช้ที่สมัครสำเร็จ
            messages.success(request, 'Your account has been created successfully!')  # แสดงข้อความสำเร็จ
            return redirect('/')  # ไปที่หน้าแรก
        else:
            messages.error(request, 'There was an error in your signup form. Please try again.')  # แสดงข้อความเมื่อเกิดข้อผิดพลาด
    else:
        form = SignUpForm()  # ฟอร์มเปล่า
    
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
                messages.error(request, 'error')
    else:
        form = AuthenticationForm()

    return render(request, 'signin.html', {'form': form})

def logout_view(request):
    logout(request)  # ฟังก์ชัน Logout จาก Django
    return redirect('signin')  # หลัง Logout ให้เปลี่ยนเส้นทางไปที่หน้า Login





@login_required(login_url='/signin/')
def page1(request):
    profile = UserProfile.objects.get(user=request.user)  # ดึงข้อมูลโปรไฟล์ของผู้ใช้
    return render(request, 'home.html', {'profile': profile,'user': request.user})

@login_required  
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

 
@login_required
def profile_page(request):
    profile = UserProfile.objects.get(user=request.user)  # ดึงข้อมูลโปรไฟล์ของผู้ใช้
    cats = Cat.objects.filter(user=request.user)  # ดึงโพสต์ที่ผู้ใช้งานปัจจุบันโพสต์
    return render(request, 'profile.html', {'profile': profile, 'cats': cats, 'user': request.user})


@login_required 
def adopt(request):
    profile = UserProfile.objects.get(user=request.user)  # ดึงข้อมูลโปรไฟล์ของผู้ใช้
    cats = Cat.objects.all()  # ดึงข้อมูลแมวทั้งหมด
    return render(request, 'adopt.html', {'profile': profile,'cats': cats})

@login_required
def cat_detail(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    return render(request, 'cat_detail.html', {'cat': cat})

@login_required
def post_cat(request):
    profile = UserProfile.objects.get(user=request.user)  # ดึงข้อมูลโปรไฟล์ของผู้ใช้
    if request.method == 'POST':
        form = CatPostForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user  # เชื่อมผู้โพส
            image = request.FILES.get('image')  # ดึงไฟล์ภาพจากฟอร์ม
            if image:
                cat.save_image(image)  # แปลงและบันทึกเป็น Base64
            else:
                cat.save()
            return redirect('adopt')  # กลับไปยังหน้าหลัก
    else:
        form = CatPostForm()

    return render(request, 'post.html', {'form': form,'profile': profile})


@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        picture_form = ProfilePictureUpdateForm(request.POST, request.FILES)

        if picture_form.is_valid():
            image = request.FILES.get('profile_picture')  # รับไฟล์ภาพจากฟอร์ม
            if image:
                profile.save_profile_picture(image)  # แปลงและบันทึกเป็น Base64
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')

    else:
        picture_form = ProfilePictureUpdateForm()

    return render(request, 'edit_profile.html', {
        'picture_form': picture_form,
        'profile': profile,
    })


@login_required
def match(request):
    profile = UserProfile.objects.get(user=request.user)  # ดึงข้อมูลโปรไฟล์ของผู้ใช้
    if request.method == 'POST':
        form = BirthDateForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            # ทำการประมวลผลที่นี่ (เช่น บันทึก, คำนวณ ฯลฯ)
            messages.success(request, f'Your birth date is {day}/{month}/{year}')
            return redirect('match')  # Redirect กลับมาที่หน้าเดิม
    else:
        form = BirthDateForm()
    
    return render(request, 'match.html', {'profile': profile,'form': form})

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)  # ดึงข้อมูลผู้ใช้ที่กำลังถูกเรียกดู
    profile = UserProfile.objects.get(user=user)  # ดึงโปรไฟล์ของผู้ใช้งานนี้
    cats = Cat.objects.filter(user=user)  # ดึงโพสต์แมวทั้งหมดที่ผู้ใช้โพสต์
    return render(request, 'user_profile.html', {'profile': profile, 'user': user, 'cats': cats})

@login_required
def delete_cat(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id, user=request.user)  # ตรวจสอบว่าผู้ใช้เป็นเจ้าของโพสต์
    cat.delete()
    return redirect('profile')  # หลังลบเสร็จให้กลับไปที่หน้า Profile

@login_required
def edit_cat(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id, user=request.user)  # ตรวจสอบว่าเป็นเจ้าของโพสต์
    if request.method == 'POST':
        form = CatPostForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            cat = form.save(commit=False)
            image = request.FILES.get('image')  # รับไฟล์ภาพ
            if image:
                cat.save_image(image)  # แปลงและบันทึกเป็น Base64
            cat.save()
            return redirect('profile')  # กลับไปที่ Profile หลังแก้ไขเสร็จ
    else:
        form = CatPostForm(instance=cat)

    return render(request, 'edit_cat.html', {'form': form, 'cat': cat})
