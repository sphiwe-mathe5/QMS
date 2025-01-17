
from django import forms
from .models import EmailTemplate

class EmailForm(forms.Form):
    recipient = forms.CharField(  
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email addresses (separated by commas)'
        })
    )
    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email subject'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type your message here',
            'rows': 5
        })
    )

    def clean_recipient(self):

        data = self.cleaned_data['recipient']
        
        emails = [email.strip() for email in data.replace(';', ',').split(',')]
        
        emails = [email for email in emails if email]
        
        
        for email in emails:
            if not email:
                continue
            
            try:
                forms.EmailField().clean(email)
            except forms.ValidationError:
                raise forms.ValidationError(f'Invalid email address: {email}')
        
        if not emails:
            raise forms.ValidationError('At least one email address is required.')
            
        return emails
