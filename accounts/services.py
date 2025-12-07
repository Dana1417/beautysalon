import random
from datetime import timedelta
from django.utils import timezone
from .models import OTP, CustomUser


# ==========================================================
# 🔢 إنشاء كود OTP
# ==========================================================
def generate_otp(phone):
    code = str(random.randint(100000, 999999))

    # نحذف الأكواد القديمة لهذا الرقم
    OTP.objects.filter(phone=phone).delete()

    OTP.objects.create(phone=phone, code=code)
    return code   # مؤقتاً يرجع الكود فقط (لاحقاً SMS)
    


# ==========================================================
# 🔐 التحقق من كود OTP
# ==========================================================
def verify_otp(phone, code):
    expiration_time = timezone.now() - timedelta(minutes=5)

    otp = OTP.objects.filter(
        phone=phone,
        code=code,
        created_at__gte=expiration_time
    ).first()

    return otp is not None
