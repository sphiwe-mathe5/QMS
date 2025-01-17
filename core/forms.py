from django import forms
from django.db.models import F  # Add this import
from .models import TimeSlot

class TimeSlotForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    TIMES = [
        ('09:00 - 10:00', '09:00 - 10:00'),
        ('10:00 - 11:00', '10:00 - 11:00'),
        ('11:00 - 12:00', '11:00 - 12:00'),
        ('13:00 - 14:00', '13:00 - 14:00'),
        ('14:00 - 15:00', '14:00 - 15:00'),
        ('15:00 - 16:00', '15:00 - 16:00'),
        ('16:00 - 17:00', '16:00 - 17:00'),
    ]
    times = forms.MultipleChoiceField(
        choices=TIMES,
        widget=forms.CheckboxSelectMultiple
    )

# forms.py
class BookingForm(forms.Form):
    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.none(),
        empty_label="Select a time slot",
        label="Available Time Slots"
    )
    
    def __init__(self, date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if date:
            self.fields['time_slot'].queryset = TimeSlot.objects.filter(
                date=date,
                booked_count__lt=F('capacity')
            )
            # Customize how the options are displayed
            self.fields['time_slot'].label_from_instance = lambda obj: f"{obj.time} ({obj.available_slots()} slots available)"
