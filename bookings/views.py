from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TimeSlot, Booking
from datetime import date


# ============================================================
# 1) اختيار الخدمة
# ============================================================
def select_service_view(request):
    """الخطوة الأولى: اختيار الخدمة."""
    if request.method == "POST":
        service = request.POST.get("service")

        if not service:
            messages.error(request, "يرجى اختيار الخدمة.")
            return redirect("bookings:select_service")

        request.session["service"] = {"name": service}
        return redirect("bookings:select_date_time")

    return render(request, "services.html")


# ============================================================
# 2) اختيار التاريخ والوقت
# ============================================================
def select_date_time_view(request):
    """الخطوة الثانية: اختيار تاريخ ووقت الموعد."""
    if not request.session.get("service"):
        messages.error(request, "يرجى اختيار الخدمة أولاً.")
        return redirect("bookings:select_service")

    times = TimeSlot.objects.all().order_by("time")

    if request.method == "POST":
        date_val = request.POST.get("date")
        time_str = request.POST.get("time")

        if not date_val or not time_str:
            messages.error(request, "يرجى اختيار التاريخ والوقت.")
            return redirect("bookings:select_date_time")

        request.session["selected_date"] = date_val
        request.session["selected_time"] = time_str

        return redirect("bookings:confirm_booking")

    return render(request, "booking_date_time.html", {"times": times})


# ============================================================
# 3) تأكيد الحجز قبل الإنشاء
# ============================================================
def confirm_booking_view(request):
    """عرض تفاصيل الموعد قبل التأكيد."""
    service = request.session.get("service")
    date_val = request.session.get("selected_date")
    time_str = request.session.get("selected_time")

    if not service or not date_val or not time_str:
        messages.error(request, "يرجى إكمال الخطوات.")
        return redirect("bookings:select_service")

    return render(request, "confirm.html", {
        "service": service,
        "date": date_val,
        "time": time_str,
        "customer_phone": request.user.phone if request.user.is_authenticated else "غير مسجل",
    })


# ============================================================
# 4) إنشاء الحجز
# ============================================================
def complete_booking_view(request):
    """الخطوة الأخيرة: إنشاء الحجز فعلياً."""
    if not request.user.is_authenticated:
        messages.error(request, "يجب تسجيل الدخول.")
        return redirect("accounts:login")

    service = request.session.get("service")
    date_val = request.session.get("selected_date")
    time_str = request.session.get("selected_time")

    if not service or not date_val or not time_str:
        messages.error(request, "حدث خطأ.. يرجى إعادة العملية.")
        return redirect("bookings:select_service")

    slot = TimeSlot.objects.filter(time=time_str).first()
    if not slot:
        messages.error(request, "الوقت المحدد غير موجود.")
        return redirect("bookings:select_date_time")

    Booking.objects.create(
        user=request.user,
        service=service["name"],
        date=date_val,
        time=slot,
        staff=None,
        status="confirmed",
    )

    # تنظيف الجلسة
    for key in ("service", "selected_date", "selected_time", "edit_booking_id"):
        request.session.pop(key, None)

    return redirect("bookings:booking_success")


# ============================================================
# 5) صفحة النجاح
# ============================================================
def booking_success_view(request):
    """عرض آخر حجز ناجح."""
    latest_booking = None
    if request.user.is_authenticated:
        latest_booking = Booking.objects.filter(user=request.user).order_by("-created_at").first()

    return render(request, "booking_success.html", {
        "booking": latest_booking
    })


# ============================================================
# 6) صفحة جميع الحجوزات
# ============================================================
def my_bookings_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    bookings = Booking.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_bookings.html", {"bookings": bookings})


# ============================================================
# 7) إلغاء الحجز
# ============================================================
def cancel_booking(request, booking_id):
    """إلغاء حجز معين."""
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    booking = Booking.objects.filter(id=booking_id, user=request.user).first()

    if not booking:
        messages.error(request, "الحجز غير موجود.")
        return redirect("accounts:dashboard")

    booking.status = "canceled"
    booking.save()

    messages.success(request, "تم إلغاء الحجز بنجاح.")
    return redirect("accounts:dashboard")


# ============================================================
# 8) تعديل الموعد (إعادة اختيار الوقت)
# ============================================================
def edit_booking(request, booking_id):
    """تعديل الموعد: إرسال العميل مرة أخرى لاختيار التاريخ والوقت."""
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    booking = Booking.objects.filter(id=booking_id, user=request.user).first()

    if not booking:
        messages.error(request, "الحجز غير موجود.")
        return redirect("accounts:dashboard")

    # وضع معلومات الحجز القديم داخل الجلسة
    request.session["service"] = {"name": booking.service}
    request.session["edit_booking_id"] = booking.id

    return redirect("bookings:select_date_time")
