from django.urls import path
from .views import (
    login_page,
    otp_verify_view,
    send_otp,
    verify_and_login,
)

app_name = "accounts"

urlpatterns = [

    # -------------------------------------------------
    # 1) صفحة تسجيل الدخول (إدخال رقم الجوال)
    # -------------------------------------------------
    path("login/", login_page, name="login_page"),

    # -------------------------------------------------
    # 2) صفحة إدخال رمز OTP بعد إرسال الكود
    # -------------------------------------------------
    path("otp-verify/", otp_verify_view, name="otp_verify"),

    # -------------------------------------------------
    # 3) API إرسال كود التحقق (OTP)
    # -------------------------------------------------
    path("send-otp/", send_otp, name="send_otp"),

    # -------------------------------------------------
    # 4) API التحقق من الكود وتسجيل المستخدم
    # -------------------------------------------------
    path("verify/", verify_and_login, name="verify_otp"),
]
