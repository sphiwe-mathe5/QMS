from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core import views
from core.project.settings import ADMIN_PATH
from core.views import index, optout,cancel_booking, guide



urlpatterns = [
    path('', index, name='index'),
    path('accounts/', include("allauth.urls")),
    path('admin/', admin.site.urls),
    path('', include('submit.urls')),
    path('emails/', include('emails.urls')),
    path('bookings/my/', views.my_bookings, name='my_bookings'),
    path('slots/create/', views.create_slots, name='create_slots'),
    path('slots/', views.slot_list, name='slot_list'),
    path('guide/', views.guide, name='guide'),
    path('slots/book/', views.book_slot, name='book_slot'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('bookings/history/', views.bookings_history, name='bookings_history'),
    path('bookings/manage/', views.manage_bookings, name='manage_bookings'),
    path('bookings/validate/<int:booking_id>/', views.validate_booking, name='validate_booking'),
    path('optout/', optout, name='optout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='submit/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='submit/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='submit/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='submit/password_reset_complete.html'),
         name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
