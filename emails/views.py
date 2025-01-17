
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmailForm
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def is_admin(user):
    if not user.is_staff:
        raise PermissionDenied("You don't have permission to access this page.")
    return True

@user_passes_test(is_admin)
@login_required
def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_list = form.cleaned_data['recipient']  
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email='nazireemathe@gmail.com',
                    recipient_list=recipient_list,  
                    fail_silently=False,
                )
                
                messages.success(request, f'Email sent successfully to {len(recipient_list)} recipients!')
                return redirect('send_email')
            except Exception as e:
                messages.error(request, f'Failed to send email: {str(e)}')
    else:
        form = EmailForm()
    
    return render(request, 'emails/send_email.html', {'form': form})

