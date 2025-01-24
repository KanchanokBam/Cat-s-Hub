from django.db import models
from django.contrib.auth.models import User
from datetime import date
import base64, random

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture_base64 = models.TextField(blank=True, null=True)  # รูปภาพในรูปแบบ Base64

    def get_profile_picture(self):
        """คืนค่า Base64 สำหรับใช้ใน <img> หรือ None หากไม่มีรูป"""
        if self.profile_picture_base64:
            return f"data:image/jpeg;base64,{self.profile_picture_base64}"
        return None

    def save_profile_picture(self, image):
        """บันทึกรูปภาพในรูปแบบ Base64"""
        import base64
        if image:
            # แปลงรูปภาพให้เป็น Base64
            self.profile_picture_base64 = base64.b64encode(image.read()).decode('utf-8')
            self.save()  # บันทึกข้อมูลลงฐานข้อมูล

    def __str__(self):
        return self.user.username



class Cat(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    personality = models.TextField(blank=True, null=True)  # ใช้สำหรับจับคู่
    image_base64 = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cats')
    is_adopted = models.BooleanField(default=False)
    adopted_date = models.DateField(blank=True, null=True)


    def save_image(self, image):
        if image:
            self.image_base64 = base64.b64encode(image.read()).decode('utf-8')
            self.save()

    def get_image_base64(self):
        if self.image_base64:
            return f"data:image/jpeg;base64,{self.image_base64}"
        return None

    def __str__(self):
        return self.name