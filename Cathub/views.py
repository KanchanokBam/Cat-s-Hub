from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.timezone import now, timedelta
from django import forms
from django.core.exceptions import PermissionDenied
from datetime import date
from .models import Cat, User,UserProfile
from .forms import SignUpForm, CatPostForm, UsernameUpdateForm, BirthDateForm ,ProfilePictureUpdateForm,CatForm,UserForm
import base64


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
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'home.html', {'profile': profile,'user': request.user})

@login_required  
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

 
@login_required
def profile_page(request):
    profile = UserProfile.objects.get(user=request.user)
    cats = Cat.objects.filter(user=request.user)

    # สลับสถานะการรับเลี้ยงเมื่อกดปุ่ม
    if request.method == 'POST':
        cat_id = request.POST.get('cat_id')
        cat = get_object_or_404(Cat, id=cat_id, user=request.user)
        cat.is_adopted = not cat.is_adopted  # สลับสถานะ
        cat.adopted_date = date.today() if cat.is_adopted else None
        cat.save()
        return redirect('profile')

    return render(request, 'profile.html', {'profile': profile, 'cats': cats, 'user': request.user})




@login_required 
def adopt(request):
    profile = UserProfile.objects.get(user=request.user)  # ดึงข้อมูลโปรไฟล์ของผู้ใช้
    cats = Cat.objects.all()  # ดึงข้อมูลแมวทั้งหมด
    return render(request, 'adopt.html', {'profile': profile,'cats': cats})

@login_required
def cat_detail(request, cat_id):
    profile = UserProfile.objects.get(user=request.user)  # ดึงข้อมูลโปรไฟล์ของผู้ใช้
    cat = get_object_or_404(Cat, id=cat_id)
    return render(request, 'cat_detail.html', {'cat': cat,'profile': profile})

@login_required
def post_cat(request):
    profile = UserProfile.objects.get(user=request.user)  # ดึงข้อมูลโปรไฟล์ของผู้ใช้
    
    if request.method == 'POST':
        form = CatPostForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user  # เชื่อมผู้โพส
            
            # ตรวจสอบหาก personality ไม่ได้เลือก
            if cat.personality == '':
                cat.personality = None
            
            # จัดการไฟล์ภาพที่อัปโหลด
            image = request.FILES.get('image')  # ดึงไฟล์ภาพจากฟอร์ม
            if image:
                cat.save_image(image)  # แปลงและบันทึกเป็น Base64
            else:
                cat.save()  # บันทึกแมวลงฐานข้อมูล
            
            return redirect('adopt')  # กลับไปยังหน้าหลัก
    else:
        form = CatPostForm()

    return render(request, 'post.html', {'form': form, 'profile': profile})



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
            return redirect('edit_cat', cat_id=cat.id)  # กลับไปที่หน้า edit_cat ของผู้ใช้งานทั่วไป
    else:
        form = CatPostForm(instance=cat)

    return render(request, 'edit_cat.html', {'form': form, 'cat': cat})


@login_required
def statistics(request):
    profile = UserProfile.objects.get(user=request.user)  # ดึงข้อมูลโปรไฟล์ของผู้ใช้
    today = date.today()
    daily_adoption = Cat.objects.filter(adopted_date=today).count()
    return render(request, 'statistics.html', {'daily_adoption': daily_adoption, 'profile': profile})


@login_required
def find_cat(request):
    profile = UserProfile.objects.get(user=request.user)  # ดึงข้อมูลโปรไฟล์ของผู้ใช้
    if request.method == 'POST':
        # รับค่าจากผู้ใช้
        personality = request.POST.get('personality')
        age = request.POST.get('age')
        breed = request.POST.get('breed')
        color = request.POST.get('color')

        # ดึงแมวทั้งหมดจากฐานข้อมูล
        cats = Cat.objects.all()

        # คำนวณคะแนน (scoring)
        scored_cats = []
        for cat in cats:
            score = 0

            # เปรียบเทียบ personality
            if personality and personality.lower() in (cat.personality or '').lower():
                score += 1

            # เปรียบเทียบอายุ
            if age:
                if age == 'kitten' and cat.age < 1:
                    score += 1
                elif age == 'adult' and 1 <= cat.age < 7:
                    score += 1
                elif age == 'senior' and cat.age >= 7:
                    score += 1

            # เปรียบเทียบ breed
            if breed and breed.lower() in (cat.breed or '').lower():
                score += 1

            # เปรียบเทียบ color
            if color and color.lower() in (cat.color or '').lower():
                score += 1

            # เพิ่มแมวพร้อมคะแนนเข้าไปในรายการ
            scored_cats.append({
                'cat': cat,
                'score': score
            })

        # กรองแมวที่มีคะแนนตั้งแต่ 3 ข้อขึ้นไป
        scored_cats = [entry for entry in scored_cats if entry['score'] >= 3]

        # จัดลำดับตามคะแนน (เรียงจากคะแนนสูงสุด -> ต่ำสุด)
        scored_cats = sorted(scored_cats, key=lambda x: x['score'], reverse=True)

        # เตรียมข้อมูลสำหรับ JSON Response
        cat_list = [
            {
                'id': entry['cat'].id,  # ต้องมี 'id' อยู่ใน JSON
                'name': entry['cat'].name,
                'age': entry['cat'].age,
                'breed': entry['cat'].breed or 'Unknown',
                'color': entry['cat'].color or 'Unknown',
                'image_url': entry['cat'].get_image_base64(),
            }
            for entry in scored_cats
        ]

        return JsonResponse({'cats': cat_list})

    elif request.method == 'GET':
        # ดึงข้อมูล breed และ color เพื่อนำไปแสดงใน Dropdown
        breeds = Cat.objects.values_list('breed', flat=True).distinct()
        colors = Cat.objects.values_list('color', flat=True).distinct()
        personalitys = Cat.objects.values_list('personality', flat=True).distinct()

        return render(request, 'find_cat.html', {
            'breeds': breeds,
            'colors': colors,
            'personalitys': personalitys,
            'profile': profile
        })

    return HttpResponseBadRequest('Invalid request method.')

# Mapping ระหว่างราศีและนิสัยของแมว
ZODIAC_PERSONALITY_MAP = {
    'Aries': ['playful', 'adventurous', 'energetic'],
    'Taurus': ['calm', 'affectionate', 'lazy'],
    'Gemini': ['curious', 'talkative', 'active'],
    'Cancer': ['affectionate', 'loyal', 'gentle'],
    'Leo': ['confident', 'bold', 'attention-seeking'],
    'Virgo': ['neat', 'smart', 'easygoing'],
    'Libra': ['friendly', 'peaceful', 'charming'],
    'Scorpio': ['independent', 'intense', 'unique'],
    'Sagittarius': ['adventurous', 'playful', 'independent'],
    'Capricorn': ['calm', 'loyal', 'easygoing'],
    'Aquarius': ['quirky', 'creative', 'independent'],
    'Pisces': ['gentle', 'dreamy', 'affectionate'],
}


# ฟังก์ชันคำนวณจักรราศี
def get_zodiac_sign(day, month):
    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return 'Aquarius'
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return 'Pisces'
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return 'Aries'
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return 'Taurus'
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return 'Gemini'
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return 'Cancer'
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return 'Leo'
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return 'Virgo'
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return 'Libra'
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return 'Scorpio'
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return 'Sagittarius'
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return 'Capricorn'

# View สำหรับจับคู่แมว
@login_required
def match(request):
    profile = UserProfile.objects.get(user=request.user)  # ดึงข้อมูลโปรไฟล์ของผู้ใช้
    if request.method == 'POST':
        form = BirthDateForm(request.POST)
        if form.is_valid():
            # รับวันเกิดจากฟอร์ม
            birth_date = form.cleaned_data['birth_date']
            day = birth_date.day
            month = birth_date.month

            # คำนวณจักรราศี
            zodiac_sign = get_zodiac_sign(day, month)

            # ดึงนิสัยแมวที่เหมาะสมกับจักรราศี
            personalities = ZODIAC_PERSONALITY_MAP.get(zodiac_sign, [])

            # ค้นหาแมวที่มีนิสัยตรงกับจักรราศี
            matched_cats = Cat.objects.filter(
                personality__icontains=personalities[0]
            )

            # ส่งผลลัพธ์ไปยังหน้าแสดงผล
            return render(request, 'match_result.html', {
                'zodiac_sign': zodiac_sign,
                'matched_cats': matched_cats,
                'profile': profile
            })
        else:
            messages.error(request, "Invalid input. Please try again.")
    else:
        form = BirthDateForm()

    return render(request, 'match.html', {'form': form,'profile': profile})





# Check if user is admin

def is_admin(user):
    if user.is_staff or user.is_superuser:
        return True
    raise PermissionDenied("You do not have permission to access this page.")

# Admin dashboard
@user_passes_test(is_admin)
def admin_dashboard(request):
    today = now().date()

    # จำนวนแมวที่ถูก adopt วันนี้ (เปลี่ยนจาก adopted เป็น is_adopted)
    adopted_cats_today = Cat.objects.filter(is_adopted=True, adopted_date=today).count()

    # จำนวนผู้ใช้งานที่เข้าเว็บ (สมมติว่าใช้ last_login เป็นตัววัด)
    users_logged_in_today = User.objects.filter(last_login__date=today).count()

    # จำนวนโพสต์แมวทั้งหมดในระบบ
    total_cats_posted = Cat.objects.count()

    context = {
        'adopted_cats_today': adopted_cats_today,
        'users_logged_in_today': users_logged_in_today,
        'total_cats_posted': total_cats_posted,
        'users': User.objects.all(),
        'cats': Cat.objects.all(),
    }
    return render(request, 'admin_dashboard.html', context)

# Add new cat
@user_passes_test(is_admin)
def add_cat(request):
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save(commit=False)  # หยุดก่อนบันทึก
            cat.user = request.user  # กำหนดค่า user
            
            # ถ้ามีอัปโหลดไฟล์ภาพ ให้แปลงเป็น Base64
            image = request.FILES.get('image')
            if image:
                cat.image_base64 = base64.b64encode(image.read()).decode('utf-8')
            
            cat.save()  # บันทึกลงฐานข้อมูล
            messages.success(request, 'Cat added successfully!')
            return redirect('admin_dashboard')
    else:
        form = CatForm()
    return render(request, 'admin_add_cat.html', {'form': form})


@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully!')
            return redirect('admin_dashboard')
    else:
        form = UserForm()
    return render(request, 'admin_add_user.html', {'form': form})

@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # บันทึกข้อมูลผู้ใช้
            user = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                # แปลงรูปภาพให้เป็น Base64
                image = request.FILES['profile_picture']
                user_profile.profile_picture_base64 = base64.b64encode(image.read()).decode('utf-8')
                user_profile.save()
            user.save()
            messages.success(request, 'User updated successfully.')
            return redirect('admin_dashboard')
    else:
        form = UserForm(instance=user)

    return render(request, 'admin_edit_user.html', {
        'form': form,
        'user': user,
        'profile_picture': user_profile.get_profile_picture()  # ส่งรูปภาพ Base64 ไปยังเทมเพลต
    })


# Edit cat
@user_passes_test(is_admin)
def edit_cat_admin(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)

    if not request.user.is_staff and not request.user.is_superuser:
        raise PermissionDenied("Only admin users can access this page.")

    if request.method == 'POST':
        form = CatPostForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            cat = form.save(commit=False)
            image = request.FILES.get('image')
            if image:
                cat.save_image(image)
            cat.save()
            messages.success(request, 'Cat updated successfully.')
            return redirect('admin_dashboard')
    else:
        form = CatPostForm(instance=cat)

    return render(request, 'admin_edit_cat.html', {'form': form, 'cat': cat})


@user_passes_test(is_admin)
def delete_user(request, user_id):
    """
    ลบผู้ใช้งานโดย Admin
    """
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def admin_delete_cat(request, cat_id):
    # ดึงข้อมูลแมวตาม ID หรือแสดง 404 ถ้าไม่เจอ
    cat = get_object_or_404(Cat, id=cat_id)
    cat.delete()
    messages.success(request, f"Cat with ID {cat_id} has been deleted successfully.")
    return redirect('admin_dashboard')