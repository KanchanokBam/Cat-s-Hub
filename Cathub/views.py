from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.templatetags.static import static
from django.contrib import messages
from django.utils.timezone import now
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.sessions.models import Session
from django.views.generic.detail import DetailView
from datetime import date, timedelta
from django.db.models import Count
from .models import Cat, UserProfile, User,Notification,ContactRequest,FeaturedProject
import json
from .forms import SignUpForm, AuthenticationForm, CatPostForm, ProfilePictureUpdateForm,BirthDateForm,UserForm, CatForm,FeaturedProjectForm
from django.utils import translation
from django.utils.translation import gettext as _


def set_language(request):
    language = request.POST.get('language')  # รับค่าภาจาก form
    translation.activate(language)  # ใช้งานภาษาใหม่
    request.session['django_language'] = language  # เก็บภาษาลงใน session
    return redirect(request.META.get('HTTP_REFERER', '/'))  # เปลี่ยนเส้นทางไปหน้าก่อนหน้า


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('คุณลงทะเบียนสำเร็จ!'))
            return redirect('signin')
        else:
            messages.error(request, _('เกิดข้อผิดพลาด กรุณาลองอีกครั้ง'))
        return render(request, 'signup.html', {'form': form})

class SignInView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, _('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'))
        return render(request, 'signin.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('signin')

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        cats = list(Cat.objects.all())
        projects = FeaturedProject.objects.all()
        import random
        random.shuffle(cats)
        return render(request, 'home.html', {
            'profile': profile, 
            'user': request.user, 
            'cats': cats[:7],
            'projects': projects
        })

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = FeaturedProject
    template_name = 'project_detail.html'
    context_object_name = 'project'

    # เพิ่มตรงนี้เพื่อส่งข้อมูล profile ไปยัง template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        return context

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html', {'user': request.user})

class CatDetailView(LoginRequiredMixin, View):
    def get(self, request, cat_id):
        profile = UserProfile.objects.get(user=request.user)
        cat = get_object_or_404(Cat, id=cat_id)
        return render(request, 'cat_detail.html', {'cat': cat, 'profile': profile})

class ProfilePageView(LoginRequiredMixin, View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        cats = Cat.objects.filter(user=request.user)
        return render(request, 'profile.html', {'profile': profile, 'cats': cats, 'user': request.user})

    def post(self, request):
        cat_id = request.POST.get('cat_id')
        cat = get_object_or_404(Cat, id=cat_id, user=request.user)
        cat.is_adopted = not cat.is_adopted
        cat.adopted_date = date.today() if cat.is_adopted else None
        cat.save()
        return redirect('profile')
    
class AdoptView(LoginRequiredMixin, View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        cats = Cat.objects.all()
        return render(request, 'adopt.html', {
            'profile': profile,
            'cats': cats,
        })


class PostCatView(LoginRequiredMixin, View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        form = CatPostForm()  # ฟอร์มที่อัปเดตแล้ว
        return render(request, 'post.html', {'form': form, 'profile': profile})

    def post(self, request):
        profile = UserProfile.objects.get(user=request.user)
        form = CatPostForm(request.POST, request.FILES)  # ใช้ฟอร์มที่รับข้อมูลจาก POST
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user  # ตั้งค่าผู้ใช้
            cat.save()  # บันทึกข้อมูล
            return redirect('adopt')
        return render(request, 'post.html', {'form': form, 'profile': profile})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        picture_form = ProfilePictureUpdateForm()
        return render(request, 'edit_profile.html', {'picture_form': picture_form, 'profile': profile})

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        picture_form = ProfilePictureUpdateForm(request.POST, request.FILES)  # ใช้ request.FILES เพื่อรองรับการอัปโหลดไฟล์
        phone = request.POST.get('phone')
        line = request.POST.get('line')
        if picture_form.is_valid():
            image = request.FILES.get('profile_picture')  # รับไฟล์ภาพที่อัปโหลด
            if image:
                profile.profile_picture = image  # เก็บไฟล์ภาพลงใน profile_picture
        profile.phone = phone
        profile.line = line
        profile.save()  # บันทึกข้อมูลโปรไฟล์
        messages.success(request, _('คุณอัปเดตโปรไฟล์แล้ว'))
        return redirect('profile')



class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = UserProfile.objects.get(user=user)
        cats = Cat.objects.filter(user=user)
        return render(request, 'user_profile.html', {'profile': profile, 'user': user, 'cats': cats})

class DeleteCatView(LoginRequiredMixin, View):
    def post(self, request, cat_id):
        cat = get_object_or_404(Cat, id=cat_id, user=request.user)
        cat.delete()
        return redirect('profile')

class EditCatView(LoginRequiredMixin, View):
    def get(self, request, cat_id):
        cat = get_object_or_404(Cat, id=cat_id, user=request.user)
        form = CatPostForm(instance=cat)
        return render(request, 'edit_cat.html', {'form': form, 'cat': cat})

    def post(self, request, cat_id):
        cat = get_object_or_404(Cat, id=cat_id, user=request.user)
        form = CatPostForm(request.POST, request.FILES, instance=cat)  
        if form.is_valid():
            cat = form.save()
            return redirect('edit_cat', cat_id=cat.id)
        return render(request, 'edit_cat.html', {'form': form, 'cat': cat})

class StatisticsView(LoginRequiredMixin, View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        today = date.today()
        daily_adoption = Cat.objects.filter(adopted_date=today).count()
        return render(request, 'statistics.html', {'daily_adoption': daily_adoption, 'profile': profile})

class FindCatView(LoginRequiredMixin, View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        breeds = Cat.objects.values_list('breed', flat=True).distinct()
        colors = Cat.objects.values_list('color', flat=True).distinct()
        personalitys = Cat.objects.values_list('personality', flat=True).distinct()
        return render(request, 'find_cat.html', {
            'breeds': breeds,
            'colors': colors,
            'personalitys': personalitys,
            'profile': profile
        })

    def post(self, request):
        profile = UserProfile.objects.get(user=request.user)
        personality = request.POST.get('personality')
        age_group = request.POST.get('age_group')  
        breed = request.POST.get('breed')
        color = request.POST.get('color')

        cats = Cat.objects.all()
        scored_cats = []

        for cat in cats:
            score = 0
            
            # ตรวจสอบ personality
            if personality and personality.lower() in (cat.personality or '').lower():
                score += 1

            # ตรวจสอบ age_group
            if age_group:
                if age_group == 'kitten' and cat.age_group == 'kitten':
                    score += 1
                elif age_group == 'adult' and cat.age_group == 'adult':
                    score += 1
                elif age_group == 'senior' and cat.age_group == 'senior':
                    score += 1

            # ตรวจสอบ breed
            if breed and breed.lower() in (cat.breed or '').lower():
                score += 1

            # ตรวจสอบ color
            if color and color.lower() in (cat.color or '').lower():
                score += 1

            # เก็บผลคะแนนที่ผ่านเกณฑ์
            scored_cats.append({'cat': cat, 'score': score})

        # กรองแมวที่ได้คะแนนมากกว่าหรือเท่ากับ 3
        scored_cats = [entry for entry in scored_cats if entry['score'] >= 3]

        # จัดลำดับแมวตามคะแนน
        scored_cats.sort(key=lambda x: x['score'], reverse=True)

        # ส่งผลลัพธ์แมวที่ตรงกับคำตอบ
        cat_list = [
            {
                'id': entry['cat'].id,
                'name': entry['cat'].name,
                'age_group': entry['cat'].age_group,  # ใช้ age_group แทน age
                'breed': entry['cat'].breed or 'Unknown',
                'color': entry['cat'].color or 'Unknown',
                'image_url': entry['cat'].image.url if entry['cat'].image else None,  # ดึง URL ของรูปภาพจาก ImageField
            }
            for entry in scored_cats
        ]

        return JsonResponse({'cats': cat_list})


class MatchView(LoginRequiredMixin, View):
    ZODIAC_PERSONALITY_MAP = {
        'เมษ': ['ขี้เล่น', 'กระตือรือร้น'],
        'พฤษภ': ['สงบ', 'ขี้เกียจ'],
        'เมถุน': ['อยากรู้อยากเห็น'],
        'กรกฎ': ['อ่อนโยน'],
        'สิงห์': ['กล้าหาญ'],
        'กันย์': ['ฉลาด', 'สบายๆ'],
        'ตุลย์': ['เป็นมิตร', 'สงบ'],
        'พิจิก': ['ชอบอิสระ','เป็นตัวของตัวเอง'],
        'ธนู': ['ขี้เล่น', 'ชอบอิสระ'],
        'มังกร': ['สงบ','สบายๆ'],
        'กุมภ์': ['ชอบอิสระ'],
        'มีน': ['อ่อนโยน'],
    }

    ZODIAC_DETAILS = {
        zodiac: {"image": static(f"images/zodiac/{zodiac}.png")}
        for zodiac in ZODIAC_PERSONALITY_MAP.keys()
    }

    def get_zodiac_sign(self, day, month):
        zodiac_ranges = [
            ((1, 20), (2, 18), 'กุมภ์'), ((2, 19), (3, 20), 'มีน'),
            ((3, 21), (4, 19), 'เมษ'), ((4, 20), (5, 20), 'พฤษภ'),
            ((5, 21), (6, 20), 'เมถุน'), ((6, 21), (7, 22), 'กรกฎ'),
            ((7, 23), (8, 22), 'สิงห์'), ((8, 23), (9, 22), 'กันย์'),
            ((9, 23), (10, 22), 'ตุลย์'), ((10, 23), (11, 21), 'พิจิก'),
            ((11, 22), (12, 21), 'ธนู'), ((12, 22), (1, 19), 'มังกร'),
        ]
        for start, end, sign in zodiac_ranges:
            if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
                return sign
        return 'มังกร'

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        form = BirthDateForm()
        return render(request, 'match.html', {'form': form, 'profile': profile})

    def post(self, request):
        profile = UserProfile.objects.get(user=request.user)
        form = BirthDateForm(request.POST)
        if form.is_valid():
            birth_date = form.cleaned_data['birth_date']
            zodiac_sign = self.get_zodiac_sign(birth_date.day, birth_date.month)
            zodiac_image = self.ZODIAC_DETAILS.get(zodiac_sign, {}).get('image', '')
            personalities = self.ZODIAC_PERSONALITY_MAP.get(zodiac_sign, [])
            matched_cats = Cat.objects.filter(personality__icontains=personalities[0] if personalities else '')
            return render(request, 'match_result.html', {
                'zodiac_sign': zodiac_sign,
                'zodiac_image': zodiac_image,
                'matched_cats': matched_cats,
                'profile': profile
            })
        messages.error(request, "กรุณาลองอีกครั้ง")
        return render(request, 'match.html', {'form': form, 'profile': profile})
class NotificationListView(LoginRequiredMixin, View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
        return render(request, 'notifications.html', {'notifications': notifications, 'profile': profile})

class MarkNotificationAsReadView(LoginRequiredMixin, View):
    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})

class ClearNotificationsView(LoginRequiredMixin, View):
    def post(self, request):
        Notification.objects.filter(user=request.user).delete()
        return redirect('notifications')

class GetNotificationCountView(LoginRequiredMixin, View):
    def get(self, request):
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({'notification_count': unread_count})

class RequestContactView(LoginRequiredMixin, View):
    def post(self, request, cat_id):
        user = request.user
        cat = get_object_or_404(Cat, id=cat_id)
        owner = cat.user
        contact_request = ContactRequest.objects.create(user=user, cat=cat)
        Notification.objects.create(
            user=owner,
            message=f"{user.username} ได้ขอข้อมูลติดต่อสำหรับแมวของคุณ {cat.name}.",
            contact_request=contact_request
        )
        return JsonResponse({'success': True})

class ApproveContactView(LoginRequiredMixin, View):
    def get(self, request, contact_request_id):
        return self._handle_approval(request, contact_request_id)

    def post(self, request, contact_request_id):
        return self._handle_approval(request, contact_request_id)

    def _handle_approval(self, request, contact_request_id):
        contact_request = get_object_or_404(ContactRequest, id=contact_request_id, cat__user=request.user)

        if contact_request.status != 'pending':
            messages.error(request, _("คำขอนี้ได้รับการดำเนินการแล้ว"))
            return redirect('profile')  # << เปลี่ยนเป็น redirect หน้าโปรไฟล์

        contact_request.status = 'approved'
        contact_request.save()

        owner_profile = UserProfile.objects.get(user=request.user)
        Notification.objects.create(
            user=contact_request.user,
            contact_request=contact_request,
            message=f"ข้อมูลติดต่อสำหรับคุณ {contact_request.cat.name} เบอร์โทร - {owner_profile.phone or 'ไม่พร้อมใช้งาน'}, ไลน์ - {owner_profile.line or 'ไม่พร้อมใช้งาน'}"
        )

        messages.success(request, _("การขอข้อมูลได้รับการยืนยันแล้ว"))
        return redirect('profile') 

class DeclineContactView(LoginRequiredMixin, View):
    def post(self, request, contact_request_id):
        contact_request = get_object_or_404(ContactRequest, id=contact_request_id, cat__user=request.user)
        if contact_request.status != 'pending':
            messages.error(request, _("คำขอนี้ได้รับการดำเนินการแล้ว"))
            return redirect('notifications')
        contact_request.status = 'declined'
        contact_request.save()
        Notification.objects.create(
            user=contact_request.user,
            contact_request=contact_request,
            message=f"คำขอข้อมูลติดต่อของคุณสำหรับ {contact_request.cat.name} ถูกปฏิเสธ"
        )
        messages.success(request, _("คำขอข้อมูลติดต่อถูกปฏิเสธเรียบร้อยแล้ว"))
        return redirect('notifications')

class ViewContactInfoView(LoginRequiredMixin, View):
    def get(self, request, request_id):
        contact_request = get_object_or_404(ContactRequest, id=request_id, user=request.user)
        if contact_request.status != 'approved':
            return JsonResponse({'error': _('คำขอข้อมูลติดต่อยังไม่ได้รับการอนุมัติ')}, status=403)
        owner_profile = contact_request.cat.user.profile
        return JsonResponse({
            'owner_name': contact_request.cat.user.username,
            'phone': owner_profile.phone or 'ไม่พร้อมใช้งาน',
            'line': owner_profile.line or 'ไม่พร้อมใช้งาน'
        })

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        raise PermissionDenied(_("คุณไม่มีสิทธิ์เข้าถึงหน้านี้"))

class AdminDashboardView(AdminRequiredMixin, View):
    def get(self, request):
        today = now().date()
        past_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

        active_sessions = Session.objects.filter(expire_date__gte=now())
        user_ids = [s.get_decoded().get('_auth_user_id') for s in active_sessions]
        users_logged_in_today = User.objects.filter(id__in=user_ids).count()

        users = User.objects.all()
        cats = Cat.objects.all()
        adopted_cats_today = Cat.objects.filter(is_adopted=True, adopted_date=today).count()
        total_cats_posted = Cat.objects.count()

        # เพิ่มการดึงข้อมูล FeaturedProject
        projects = FeaturedProject.objects.all()

        daily_users = User.objects.filter(last_login__date__gte=past_7_days[0])\
            .values('last_login__date').annotate(count=Count('id'))
        daily_user_data = {
            'dates': [day.strftime('%d %b') for day in past_7_days],
            'counts': [next((item['count'] for item in daily_users if item['last_login__date'] == day), 0) for day in past_7_days]
        }

        daily_adopts = Cat.objects.filter(is_adopted=True, adopted_date__gte=past_7_days[0])\
            .values('adopted_date').annotate(count=Count('id'))
        daily_adopt_data = {
            'dates': [day.strftime('%d %b') for day in past_7_days],
            'counts': [next((item['count'] for item in daily_adopts if item['adopted_date'] == day), 0) for day in past_7_days]
        }

        context = {
            'users': users,
            'cats': cats,
            'adopted_cats_today': adopted_cats_today,
            'users_logged_in_today': users_logged_in_today,
            'total_cats_posted': total_cats_posted,
            'projects': projects,  # เพิ่ม projects
            'daily_user_data': json.dumps(daily_user_data),
            'daily_adopt_data': json.dumps(daily_adopt_data),
        }
        return render(request, 'admin_dashboard.html', context)

class AddCatAdminView(AdminRequiredMixin, View):
    def get(self, request):
        form = CatForm()
        return render(request, 'admin_add_cat.html', {'form': form})

    def post(self, request):
        form = CatForm(request.POST, request.FILES)  # ใช้ request.FILES เพื่อจัดการกับไฟล์
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            image = request.FILES.get('image')  # รับไฟล์ภาพจากฟอร์ม
            if image:
                cat.image = image  # เก็บภาพในฟิลด์ image ของโมเดล
            cat.save()
            messages.success(request, _('เพิ่มแมวแล้ว'))
            return redirect('admin_dashboard')
        return render(request, 'admin_add_cat.html', {'form': form})

class AddUserAdminView(AdminRequiredMixin, View):
    def get(self, request):
        form = UserForm()
        return render(request, 'admin_add_user.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('เพิ่มผู้ใช้แล้ว'))
            return redirect('admin_dashboard')
        return render(request, 'admin_add_user.html', {'form': form})

class EditUserAdminView(AdminRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        form = UserForm(instance=user)
        return render(request, 'admin_edit_user.html', {
            'form': form,
            'user': user,
            'profile_picture': user_profile.profile_picture.url if user_profile.profile_picture else None
        })

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        form = UserForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            user = form.save(commit=False)
            
            # ตรวจสอบว่าอัปโหลดรูปใหม่หรือไม่
            if 'profile_picture' in request.FILES:
                image = request.FILES['profile_picture']
                user_profile.profile_picture = image  # อัปเดตรูปภาพโปรไฟล์
                user_profile.save()  # บันทึกรูปภาพในโปรไฟล์
            user.save()  # บันทึกข้อมูลผู้ใช้
            
            messages.success(request, _('อัปเดตผู้ใช้งานแล้ว'))
            return redirect('admin_dashboard')
        
        return render(request, 'admin_edit_user.html', {'form': form, 'user': user})


class EditCatAdminView(AdminRequiredMixin, View):
    def get(self, request, cat_id):
        cat = get_object_or_404(Cat, id=cat_id)
        form = CatPostForm(instance=cat)
        return render(request, 'admin_edit_cat.html', {'form': form, 'cat': cat})

    def post(self, request, cat_id):
        cat = get_object_or_404(Cat, id=cat_id)
        form = CatPostForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            cat = form.save(commit=False)
            image = request.FILES.get('image')
            if image:
                cat.save_image(image)
            cat.save()
            messages.success(request, _('อัปเดตแมวแล้ว.'))
            return redirect('admin_dashboard')
        return render(request, 'admin_edit_cat.html', {'form': form, 'cat': cat})

class DeleteUserAdminView(AdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, _('ลบผู้ใช้เรียบร้อยแล้ว'))
        return redirect('admin_dashboard')

class DeleteCatAdminView(AdminRequiredMixin, View):
    def post(self, request, cat_id):
        cat = get_object_or_404(Cat, id=cat_id)
        cat.delete()
        messages.success(request, f"แมวไอดี {cat_id} ได้ลบแล้ว")
        return redirect('admin_dashboard')
    
# เพิ่มโครงการ
class AddProjectAdminView(AdminRequiredMixin, View):
    def get(self, request):
        form = FeaturedProjectForm()
        return render(request, 'admin_add_project.html', {'form': form})

    def post(self, request):
        form = FeaturedProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('โครงการถูกเพิ่มเรียบร้อยแล้ว'))
            return redirect('admin_dashboard')
        return render(request, 'admin_add_project.html', {'form': form})

class EditProjectAdminView(AdminRequiredMixin, View):
    def get(self, request, project_id):
        project = get_object_or_404(FeaturedProject, id=project_id)
        form = FeaturedProjectForm(instance=project)
        return render(request, 'admin_edit_project.html', {'form': form, 'project': project})

    def post(self, request, project_id):
        project = get_object_or_404(FeaturedProject, id=project_id)
        form = FeaturedProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, _('อัปเดตโครงการเรียบร้อยแล้ว'))
            return redirect('admin_dashboard')
        return render(request, 'admin_edit_project.html', {'form': form, 'project': project})

class DeleteProjectAdminView(AdminRequiredMixin, View):
    def post(self, request, project_id):
        project = get_object_or_404(FeaturedProject, id=project_id)
        project.delete()
        messages.success(request, _('ลบโครงการเรียบร้อยแล้ว'))
        return redirect('admin_dashboard')
    



