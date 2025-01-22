from django.db import models
from django.contrib.auth.models import User
import base64, random

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture_base64 = models.TextField(blank=True, null=True)  # เก็บรูปในรูปแบบ Base64

    def save_profile_picture(self, image):
        """บันทึกรูปภาพในรูปแบบ Base64"""
        if image:
            self.profile_picture_base64 = base64.b64encode(image.read()).decode('utf-8')
            self.save()

    def get_profile_picture(self):
        """คืนค่า Base64 สำหรับใช้ใน <img>"""
        if self.profile_picture_base64:
            return f"data:image/jpeg;base64,{self.profile_picture_base64}"
        return None

    def __str__(self):
        return self.user.username


class Cat(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    image_base64 = models.TextField(blank=True, null=True)  # เก็บรูปในรูปแบบ Base64
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cats')

    def save_image(self, image):
        """แปลงและบันทึกภาพในรูปแบบ Base64"""
        if image:
            self.image_base64 = base64.b64encode(image.read()).decode('utf-8')
            self.save()

    def get_image_base64(self):
        """คืนค่า Base64 สำหรับใช้ใน <img>"""
        if self.image_base64:
            return f"data:image/jpeg;base64,{self.image_base64}"
        return None

    def __str__(self):
        return self.name
