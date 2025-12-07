from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


# ==========================================================
# 🔐 Custom User Manager
# ==========================================================
class CustomUserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("يجب إدخال رقم الجوال")

        # تنظيف رقم الجوال
        phone = str(phone).strip()

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)   # حتى لو ما نستخدم كلمة مرور الآن
        user.save(using=self._db)
        return user


    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is False:
            raise ValueError("المشرف يجب أن يكون is_staff=True")

        if extra_fields.get("is_superuser") is False:
            raise ValueError("المشرف يجب أن يكون is_superuser=True")

        return self.create_user(phone, password, **extra_fields)



# ==========================================================
# 👤 Custom User Model (Login by Phone)
# ==========================================================
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    # حالـة الحساب
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "phone"         # تسجيل الدخول باستخدام رقم الجوال
    REQUIRED_FIELDS = []             # لا نحتاج أي حقول إضافية

    objects = CustomUserManager()

    def __str__(self):
        return self.phone



# ==========================================================
# 🔢 OTP Model (For verification codes)
# ==========================================================
class OTP(models.Model):
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {self.code}"
