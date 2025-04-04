from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils.timezone import now

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    line = models.CharField(max_length=50, blank=True, null=True)

    def get_profile_picture(self):
        """คืนค่าลิงก์ URL สำหรับการแสดงรูปภาพ หรือ None หากไม่มีรูป"""
        if self.profile_picture:
            return self.profile_picture.url  # คืนค่าลิงก์ของไฟล์ภาพ
        return None

    def __str__(self):
        return self.user.username



class Cat(models.Model):
    AGE_CHOICES = [
        ('kitten', 'แมวเด็ก'),  # ค่าแรกคือ value, ค่าแรกคือ label
        ('adult', 'แมวโต'),
        ('senior', 'แมวอายุมาก'),
    ]
    
    name = models.CharField(max_length=100)
    age_group = models.CharField(max_length=6, choices=AGE_CHOICES, default='kitten')  # ใช้ age_group แทน age
    breed = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    personality = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='cat_images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cats')
    is_adopted = models.BooleanField(default=False)
    adopted_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


    
class ContactRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),   # รอเจ้าของอนุมัติ
        ('approved', 'Approved'), # อนุมัติแล้ว
        ('declined', 'Declined'), # ปฏิเสธ
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests_sent")  # ผู้ที่ร้องขอข้อมูล
    cat = models.ForeignKey("Cat", on_delete=models.CASCADE)  # แมวที่ถูกขอข้อมูล
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} requested contact for {self.cat.name} - {self.status}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")  # ผู้รับแจ้งเตือน
    contact_request = models.ForeignKey(ContactRequest, on_delete=models.CASCADE, null=True, blank=True)  # เชื่อมโยงกับ ContactRequest
    message = models.TextField()  # ข้อความแจ้งเตือน
    is_read = models.BooleanField(default=False)  # สถานะว่าอ่านหรือยัง
    created_at = models.DateTimeField(default=now)  # เวลาที่แจ้งเตือน
    action_url = models.CharField(max_length=255, blank=True, null=True)  # ลิงก์ไปยังหน้าที่เกี่ยวข้อง

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
    
class FeaturedProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='featured_projects/', blank=True, null=True)

    def __str__(self):
        return self.title
