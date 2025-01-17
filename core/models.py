from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
import random
from submit.models import Profile, CustomUser
import random
import string


class TimeSlot(models.Model):
    date = models.DateField()
    time = models.CharField(max_length=50)
    capacity = models.IntegerField(default=5)
    booked_count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['date', 'time']
        
    def is_available(self):
        return self.booked_count < self.capacity
        
    def available_slots(self):
        return self.capacity - self.booked_count

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} at {self.time}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('collected', 'Collected'),
        ('cancelled', 'Cancelled')
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    reference = models.CharField(max_length=8, unique=True, blank=True)  # Remove default
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'time_slot']

    def __str__(self):
        return f"Booking {self.reference} by {self.user.username}"

    def generate_reference(self):
        # Generate a unique 8-character reference
        chars = string.ascii_uppercase + string.digits
        while True:
            reference = ''.join(random.choices(chars, k=8))
            if not Booking.objects.filter(reference=reference).exists():
                return reference

    def save(self, *args, **kwargs):
        if not self.reference:  # Only generate if reference is not set
            self.reference = self.generate_reference()
        super().save(*args, **kwargs)




