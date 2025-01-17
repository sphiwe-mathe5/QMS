from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from core.forms import BookingForm
from django.db import transaction
from core.forms import TimeSlotForm
from .models import TimeSlot, Booking
from django.db.models import F, ExpressionWrapper, IntegerField
from django.utils.dateparse import parse_date
from .models import TimeSlot
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

def index(request):
    return render(request, 'core/index.html')

def is_admin(user):
    return user.is_staff

def bookings_history(request):
    bookings = Booking.objects.all().order_by(
        'time_slot__date',
        'time_slot__time',
        '-created_at'
    )

    grouped_bookings = {}
    for booking in bookings:
        date = booking.time_slot.date
        if date not in grouped_bookings:
            grouped_bookings[date] = []
        grouped_bookings[date].append(booking)

    return render(request, 'core/bookings_history.html', {
        'grouped_bookings': grouped_bookings
    })

def create_slots(request):
    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            times = form.cleaned_data['times']

            for time in times:
                TimeSlot.objects.get_or_create(
                    date=date,
                    time=time,
                    defaults={'capacity': 5}
                )
            messages.success(request, 'Time slots created successfully!')
            return redirect('slot_list')
    else:
        form = TimeSlotForm()

    return render(request, 'core/create_slots.html', {'form': form})

def send_booking_confirmation_email(booking):

    try:
        subject = f'Booking Confirmation - Reference #{booking.reference}'
        
        message = (
            f"Dear {booking.user.username},\n\n"
            f"Your booking has been confirmed!\n\n"
            f"Booking Details:\n"
            f"Date: {booking.time_slot.date}\n"
            f"Time: {booking.time_slot.time}\n"
            f"Reference Number: {booking.reference}\n\n"
            f"Important: Please keep this reference number and present it when you arrive.\n"
            f"If you need to cancel or reschedule, please contact us as soon as possible.\n\n"
            f"Thank you for your booking!\n"
            f"Best regards,\n"
            f"{settings.SITE_NAME}"
        )
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.user.email],
            fail_silently=False,
        )
        
        return True, None
        
    except Exception as e:
        return False, str(e)

@login_required
def slot_list(request):
    filter_date = request.GET.get('filter_date', None)
    min_available_slots = request.GET.get('min_available_slots', None)

    today = timezone.now().date()
    slots = TimeSlot.objects.all().order_by('date', 'time')
    slots = slots.filter(date__gt=today)

    if filter_date:
        filter_date = parse_date(filter_date)
        slots = slots.filter(date=filter_date)

    if min_available_slots:
        min_available_slots = int(min_available_slots)
        slots = slots.annotate(
            available_slots=ExpressionWrapper(F('capacity') - F('booked_count'), output_field=IntegerField())
        )
        slots = slots.filter(available_slots=min_available_slots)

    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        time_slot = get_object_or_404(TimeSlot, id=slot_id)

        if Booking.objects.filter(user=request.user, status='pending').exists():
            messages.error(request, 'You already have a pending booking. Please wait until it is completed.')
        elif time_slot.is_available():

            booking = Booking(
                user=request.user,
                time_slot=time_slot
            )
            booking.save()
            
            time_slot.booked_count += 1
            time_slot.save()
            
            email_sent, error_message = send_booking_confirmation_email(booking)
            
            if email_sent:
                messages.success(request, 
                    f'Slot booked successfully! Your reference number is {booking.reference}. '
                    f'A confirmation email has been sent to {request.user.email}'
                )
            else:
                messages.warning(request, 
                    f'Slot booked successfully! Your reference number is {booking.reference}. '
                    f'However, we could not send the confirmation email: {error_message}. '
                    f'Please save your reference number.'
                )
            
            return redirect('my_bookings')
        else:
            messages.error(request, 'Sorry, this slot is no longer available.')

    slots_by_date = {}
    for slot in slots:
        if slot.date not in slots_by_date:
            slots_by_date[slot.date] = []
        slots_by_date[slot.date].append(slot)

    return render(request, 'core/slot_list.html', {
        'slots_by_date': slots_by_date,
        'filter_date': filter_date,
        'min_available_slots': min_available_slots,
    })

@login_required
def book_slot(request):

    if Booking.objects.filter(user=request.user, status='pending').exists():
        messages.error(request, 'You already have a pending booking. Please wait until it is completed.')
        return redirect('slot_list')

    selected_date = request.GET.get('date')

    if request.method == 'POST':
        form = BookingForm(selected_date, request.POST)
        if form.is_valid():
            time_slot = form.cleaned_data['time_slot']


            if time_slot.is_available():
                booking = Booking(
                    user=request.user,
                    time_slot=time_slot
                )
                booking.save()

                time_slot.booked_count += 1
                time_slot.save()

                messages.success(request, f'Slot booked successfully! Your reference number is {booking.reference}')
                return redirect('my_bookings')
            else:
                messages.error(request, 'Sorry, this slot is no longer available.')
    else:
        form = BookingForm(selected_date)

    return render(request, 'core/book_slot.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def manage_bookings(request):

    today = timezone.now().date()
    bookings = Booking.objects.filter(time_slot__date__gte=today)

    search_date = request.GET.get('date')
    search_reference = request.GET.get('reference')

    if search_date:
        try:
            search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
            bookings = bookings.filter(time_slot__date=search_date)
        except ValueError:
            pass

    if search_reference:
        bookings = bookings.filter(reference__icontains=search_reference)

    bookings = bookings.order_by('time_slot__date', 'time_slot__time', '-created_at')

    grouped_bookings = {}
    for booking in bookings:
        date = booking.time_slot.date
        if date not in grouped_bookings:
            grouped_bookings[date] = []
        grouped_bookings[date].append(booking)

    return render(request, 'core/manage_bookings.html', {
        'grouped_bookings': grouped_bookings
    })

@user_passes_test(lambda u: u.is_staff)
def validate_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'validate':
            booking.status = 'confirmed'
            booking.collected_at = timezone.now()
            booking.save()
            messages.success(request, f'Booking {booking.reference} marked as collected')

        elif action == 'delete':

            time_slot = booking.time_slot
            time_slot.booked_count = max(0, time_slot.booked_count - 1)
            time_slot.save()

            booking.delete()
            messages.success(request, f'Booking {booking.reference} has been deleted')

    return redirect('manage_bookings')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('time_slot__date', 'time_slot__time')
    return render(request, 'core/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':

        with transaction.atomic():

            time_slot = booking.time_slot
            if time_slot.booked_count > 0:
                time_slot.booked_count -= 1
                time_slot.save()
            
            try:
                subject = 'Booking Cancellation Confirmation'
                message = (
                    f"Dear {request.user.username},\n\n"
                    f"Your booking has been successfully cancelled.\n\n"
                    f"Booking Details:\n"
                    f"Date: {time_slot.date}\n"
                    f"Time: {time_slot.time}\n\n"
                    f"The slot is now available for other bookings.\n\n"
                    f"Thank you!\n"
                    f"Best regards,\n"
                    f"{settings.SITE_NAME}"
                )
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Failed to send cancellation email: {str(e)}")
            
            booking.delete()
            
            messages.success(request, 'Your booking has been successfully cancelled.')
        
    return redirect('my_bookings')

def optout(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')

        send_mail(
            subject='Post more inquiry',
            message=f'Email: {email}\nUsername: {username}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        messages.success(
            request,
            'Your enquiry has been received, we will send you an email soon')
        return redirect('unsubscribe')

    return redirect('index')

def guide(request):
    return render(request, 'core/guide.html')