from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # ================================
    # 🔐 User & Authentication
    # ================================
    path('accounts/', include('accounts.urls')),

    # ================================
    # 💄 Salon Catalog
    # ================================
    path('catalog/', include('catalog.urls')),

    # ================================
    # 🕒 Scheduling (Available Times)
    # ================================
    path('schedule/', include('scheduling.urls')),

    # ================================
    # 📅 Bookings System (الخَط الذي يربط صفحة التاريخ والوقت)
    # ================================
    path('bookings/', include('bookings.urls')),

    # ================================
    # 💳 Billing & Payments
    # ================================
    path('billing/', include('billing.urls')),

    # ================================
    # 🔔 Notifications
    # ================================
    path('notifications/', include('notifications_center.urls')),

    # ================================
    # 🧑‍💼 Client Portal (Home Page)
    # ================================
    path('', include('portal_client.urls')),   # الصفحة الرئيسية للعملاء

    # ================================
    # 🛠 Admin Dashboard
    # ================================
    path('dashboard/', include('control_panel.urls')),

    # ================================
    # 🧰 Django Admin Panel
    # ================================
    path('admin/', admin.site.urls),
]


# ============================================
# 📦 Static & Media Files (Development Mode)
# ============================================
if settings.DEBUG:

    # Media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Static files
    if hasattr(settings, "STATICFILES_DIRS") and settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    else:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
