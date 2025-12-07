from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
import json

from .models import CustomUser
from .services import generate_otp, verify_otp


# ==========================================================
# 📄 صفحة تسجيل الدخول (GET)
# ==========================================================
def login_page(request):
    return render(request, "login.html")


# ==========================================================
# 📄 صفحة إدخال كود OTP (GET)
# ==========================================================
def otp_verify_view(request):
    return render(request, "otp_verify.html")


# ==========================================================
# 🔢 إرسال كود OTP (POST)
# ==========================================================
@csrf_exempt
def send_otp(request):
    if request.method != "POST":
        return JsonResponse({"error": "طريقة الطلب يجب أن تكون POST"}, status=405)

    # قراءة JSON من الطلب
    try:
        body_data = request.body.decode("utf-8")
        data = json.loads(body_data)
    except Exception:
        return JsonResponse({"error": "صيغة JSON غير صحيحة"}, status=400)

    phone = data.get("phone")

    if not phone:
        return JsonResponse({"error": "يرجى إدخال رقم الجوال"}, status=400)

    # توليد الكود وإرساله
    otp = generate_otp(phone)

    return JsonResponse({
        "message": "تم إرسال كود التحقق",
        "otp_debug": otp  # يظهر فقط أثناء التطوير
    }, status=200)


# ==========================================================
# 🔐 التحقق من الكود وتسجيل الدخول (POST)
# ==========================================================
@csrf_exempt
def verify_and_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "طريقة الطلب يجب أن تكون POST"}, status=405)

    # قراءة JSON من الطلب
    try:
        body_data = request.body.decode("utf-8")
        data = json.loads(body_data)
    except Exception:
        return JsonResponse({"error": "صيغة JSON غير صحيحة"}, status=400)

    phone = data.get("phone")
    code = data.get("code")

    # التحقق من البيانات
    if not phone or not code:
        return JsonResponse({"error": "رقم الجوال والكود مطلوبان"}, status=400)

    # التحقق من الكود
    if not verify_otp(phone, code):
        return JsonResponse({"error": "الكود غير صحيح أو منتهي"}, status=400)

    # إنشاء مستخدم جديد إذا لم يكن موجوداً
    user, created = CustomUser.objects.get_or_create(phone=phone)

    # تسجيل الدخول
    login(request, user)

    return JsonResponse({
        "message": "تم تسجيل الدخول بنجاح",
        "new_user": created,
        "phone": user.phone,
    }, status=200)
