from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique = models.CharField(max_length=50,null=True, blank=True)
    uucms = models.CharField(max_length=12, null=True, blank=True)


    def __str__(self):
        return self.user.username
    


    

class QRToken(models.Model):
    token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    is_scanned = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.token} - Scanned: {self.is_scanned}"

class AttendanceRecord(models.Model):
    date = models.DateField(auto_now_add=True)
    uucms = models.CharField(max_length=12,null=True)
    user = models.CharField(max_length=30,null=True)
    token = models.CharField(max_length=30,null=True)
    time = models.TimeField(auto_now_add=True)
    Attendance = models.CharField(max_length=2,null=False,default="Absent") 