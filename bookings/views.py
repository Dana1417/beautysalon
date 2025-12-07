from django.shortcuts import render, redirect
from django.contrib import messages


# ============================================================
# 1) اختيار الخدمة
# ============================================================
def select_service_view(request):
    """صفحة اختيار الخدمة (الشعر – المكياج – الأظافر)."""

    if request.method == "POST":
        service = request.POST.get("service")

        if not service:
            messages.error(request, "يرجى اختيار الخدمة.")
            return redirect("bookings:select_service")

        request.session["service"] = {"name": service}
        return redirect("bookings:select_staff")

    # ملاحظة: اسم القالب هو services.html
    return render(request, "services.html")


# ============================================================
# 2) اختيار الموظفة (اختياري)
# ============================================================
def select_staff_view(request):
    """صفحة اختيار الموظفة أو الاستمرار بدون اختيار."""

    if request.method == "POST":
        staff = request.POST.get("staff")
        request.session["staff"] = {"name": staff} if staff else None
        return redirect("bookings:select_date_time")

    return render(request, "select_staff.html")


# ============================================================
# 3) اختيار التاريخ والوقت
# ============================================================
def select_date_time_view(request):
    """صفحة اختيار التاريخ والوقت."""

    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")

        if not date or not time:
            messages.error(request, "يرجى اختيار التاريخ والوقت.")
            return redirect("bookings:select_date_time")

        request.session["selected_date"] = date
        request.session["selected_time"] = time

        return redirect("bookings:customer_info")

    return render(request, "booking_date_time.html")


# ============================================================
# 4) إدخال بيانات العميل
# ============================================================
def customer_info_view(request):
    """صفحة تعبئة بيانات العميل (الاسم – رقم الجوال)."""

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")

        if not name or not phone:
            messages.error(request, "يرجى تعبئة جميع الحقول.")
            return redirect("bookings:customer_info")

        request.session["customer_name"] = name
        request.session["customer_phone"] = phone

        return redirect("bookings:confirm_booking")

    return render(request, "customer_info.html")


# ============================================================
# 5) صفحة التأكيد قبل الحجز
# ============================================================
def confirm_booking_view(request):
    """عرض ملخص الحجز قبل الإرسال النهائي."""

    context = {
        "service": request.session.get("service"),
        "date": request.session.get("selected_date"),
        "time": request.session.get("selected_time"),
        "staff": request.session.get("staff"),
        "customer_name": request.session.get("customer_name"),
        "customer_phone": request.session.get("customer_phone"),
    }

    # منع فتح صفحة التأكيد بدون المرور بالمراحل السابقة
    if not context["service"] or not context["date"] or not context["time"]:
        messages.error(request, "يرجى إكمال الخطوات قبل صفحة التأكيد.")
        return redirect("bookings:select_service")

    return render(request, "confirm.html", context)


# ============================================================
# 6) تنفيذ الحجز النهائي
# ============================================================
def complete_booking_view(request):
    """تنفيذ الحجز النهائي."""

    # هنا مستقبلاً تضاف عملية حفظ الحجز في قاعدة البيانات
    messages.success(request, "تم الحجز بنجاح!")

    return redirect("bookings:booking_success")


# ============================================================
# 7) صفحة نجاح الحجز (التي نصممها الآن)
# ============================================================
def booking_success_view(request):
    """صفحة تم الحجز بنجاح."""

    context = {
        "service": request.session.get("service"),
        "date": request.session.get("selected_date"),
        "time": request.session.get("selected_time"),
        "staff": request.session.get("staff"),
        "customer_name": request.session.get("customer_name"),
        "customer_phone": request.session.get("customer_phone"),
        "booking_id": "2025-001",  # مؤقت — لاحقاً سنجلبها من قاعدة البيانات
    }

    return render(request, "booking_success.html", context)


# ============================================================
# 8) صفحة حجوزات العميل
# ============================================================
def my_bookings_view(request):
    bookings = []  # سيتم استبداله لاحقاً ببيانات من قاعدة البيانات
    return render(request, "my_bookings.html", {"bookings": bookings})
