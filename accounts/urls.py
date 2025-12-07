# accounts/urls.py

from django.urls import path
from .views import (
    login_page,
    otp_verify_view,
    send_otp,
    verify_and_login,
    customer_dashboard,
    services_page,       # صفحة الخدمات
    contact_page,        # صفحة تواصل معنا
)

app_name = "accounts"

urlpatterns = [

    # -------------------------------------------------
    # صفحة تسجيل الدخول (إدخال رقم الجوال)
    # -------------------------------------------------
    path("login/", login_page, name="login_page"),

    # -------------------------------------------------
    # صفحة إدخال رمز OTP
    # -------------------------------------------------
    path("otp-verify/", otp_verify_view, name="otp_verify"),

    # -------------------------------------------------
    # API: إرسال رمز OTP
    # -------------------------------------------------
    path("send-otp/", send_otp, name="send_otp"),

    # -------------------------------------------------
    # API: التحقق من الكود وتسجيل الدخول
    # -------------------------------------------------
    path("verify/", verify_and_login, name="verify_otp"),

    # -------------------------------------------------
    # صفحة الداشبورد للزبونة بعد تسجيل الدخول
    # -------------------------------------------------
    path("dashboard/", customer_dashboard, name="customer_dashboard"),

    # -------------------------------------------------
    # صفحة عرض الخدمات المتاحة للحجز
    # -------------------------------------------------
    path("services/", services_page, name="services"),

    # -------------------------------------------------
    # صفحة تواصل معنا — Contact Page
    # -------------------------------------------------
    path("contact/", contact_page, name="contact"),
]
