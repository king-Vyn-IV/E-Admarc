from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)

    # Role fields
    is_farmer = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @property
    def is_admin(self):
        return self.user.is_superuser

    @property
    def is_user(self):
        return not self.user.is_superuser


# Signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

from django.db import models

class Product(models.Model):
    productName = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantityAvailable = models.PositiveIntegerField()
    image_url = models.URLField(blank=True, null=True)  # optional

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.productName

from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]

class FarmerSubmission(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='farmer_submissions'  # <-- add this
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='farmer_submissions/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user.username}"

from django.db import models
from django.contrib.auth.models import User
from accounts.models import FarmerSubmission


# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from products.models import FarmerSubmission  # Use the correct import

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    submission = models.ForeignKey(FarmerSubmission, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'submission')

    def __str__(self):
        return f"{self.submission.name} ({self.quantity})"

    @property
    def subtotal(self):
        return self.submission.price * self.quantity



from django.db import models
from django.contrib.auth.models import User

class Submission(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='submissions/', blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

