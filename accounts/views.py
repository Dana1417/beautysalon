# accounts/views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
import json

from .models import CustomUser
from .services import generate_otp, verify_otp


# ==========================================================
# 📌 صفحة تسجيل الدخول (GET)
# ==========================================================
def login_page(request):
    """عرض صفحة إدخال رقم الجوال"""
    return render(request, "login.html")



# ==========================================================
# 📌 صفحة إدخال رمز OTP (GET)
# ==========================================================
def otp_verify_view(request):
    """عرض صفحة إدخال رمز التحقق"""
    phone = request.GET.get("phone", "")
    return render(request, "otp_verify.html", {"phone": phone})



# ==========================================================
# 📌 إرسال كود OTP (POST)
# ==========================================================
@csrf_exempt
def send_otp(request):
    """إرسال رمز التحقق إلى رقم الجوال"""
    if request.method != "POST":
        return JsonResponse({"error": "طريقة الطلب يجب أن تكون POST"}, status=405)

    # قراءة JSON من الطلب
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "صيغة JSON غير صحيحة"}, status=400)

    phone = data.get("phone")

    if not phone:
        return JsonResponse({"error": "يرجى إدخال رقم الجوال"}, status=400)

    # توليد كود التحقق
    otp = generate_otp(phone)

    return JsonResponse({
        "message": "تم إرسال كود التحقق",
        "otp_debug": otp,   # يظهر أثناء التطوير فقط
    }, status=200)



# ==========================================================
# 📌 التحقق من الكود وتسجيل الدخول (POST)
# ==========================================================
@csrf_exempt
def verify_and_login(request):
    """التحقق من كود OTP وتسجيل دخول المستخدم"""
    if request.method != "POST":
        return JsonResponse({"error": "طريقة الطلب يجب أن تكون POST"}, status=405)

    # محاولة قراءة JSON
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "صيغة JSON غير صحيحة"}, status=400)

    phone = data.get("phone")
    code = data.get("code")

    if not phone or not code:
        return JsonResponse({"error": "رقم الجوال والكود مطلوبان"}, status=400)

    # تحقق من صحة الكود
    if not verify_otp(phone, code):
        return JsonResponse({"error": "الكود غير صحيح أو منتهي"}, status=400)

    # جلب المستخدم أو إنشاؤه
    user, created = CustomUser.objects.get_or_create(phone=phone)

    # تسجيل الدخول
    login(request, user)
    request.session["customer_phone"] = user.phone

    return JsonResponse({
        "message": "تم تسجيل الدخول بنجاح",
        "new_user": created,
        "redirect": "/accounts/dashboard/"
    }, status=200)



# ==========================================================
# 📌 صفحة الداشبورد (GET)
# ==========================================================
def customer_dashboard(request):
    """صفحة لوحة العميل بعد تسجيل الدخول"""
    phone = request.session.get("customer_phone", "عميل")
    return render(request, "dashboard.html", {"phone": phone})



# ==========================================================
# 📌 صفحة قائمة الخدمات (GET)
# ==========================================================
def services_page(request):
    """عرض صفحة الخدمات"""
    return render(request, "services.html")



# ==========================================================
# 📌 صفحة تواصل معنا (GET)
# ==========================================================
def contact_page(request):
    """عرض صفحة تواصل معنا"""
    return render(request, "contact.html")
