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
    # 📅 Bookings
    # ================================
    path('bookings/', include('bookings.urls')),

    # ================================
    # 💳 Billing & Payments
    # ================================
    path('billing/', include('billing.urls')),

    # ================================
    # 🔔 Notifications Center
    # ================================
    path('notifications/', include('notifications_center.urls')),

    # ================================
    # 🧑‍💼 Client Portal (Home Page)
    # ================================
    path('', include('portal_client.urls')),   # هذا يجعل home.html تفتح للمستخدم

    # ================================
    # 🛠 Control Panel Dashboard
    # ================================
    path('dashboard/', include('control_panel.urls')),


    # ================================
    # 🧰 Django Admin
    # ================================
    path('admin/', admin.site.urls),
]


# ============================================
# 📦 Static & Media Files (Development mode)
# ============================================
if settings.DEBUG:
    # تحميل الملفات من مجلد media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # تحميل الملفات من مجلد static (داخل مجلد المشروع)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
