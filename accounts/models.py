from django.db import models
import bcrypt
import jwt
from datetime import datetime, timedelta
import os

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    patronymic = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, default=2)

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def generate_jwt(self):
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow(),
        }
        return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    
    @property
    def is_authenticated(self):
        return True  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True) 

class BusinessElement(models.Model):
    name = models.CharField(max_length=50, unique=True) 
    description = models.TextField(blank=True)

class AccessRule(models.Model):
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    business_element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)

    create_permission = models.BooleanField(default=False)

    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)

    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)

    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'business_element')
