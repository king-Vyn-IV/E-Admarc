from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    buyer = models.ForeignKey(User, related_name='buyer_transactions', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='seller_transactions', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.buyer.username} ↔ {self.seller.username})"


class Message(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} on {self.transaction.title}"

# orders/models.py

from django.db import models
from django.contrib.auth.models import User
from accounts.models import FarmerSubmission

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]

class ContactRequest(models.Model):
    buyer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_requests'
    )
    seller = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_requests'
    )
    submission = models.ForeignKey(
        FarmerSubmission, 
        on_delete=models.CASCADE,
        related_name='contact_requests'
    )
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # latest requests first

    def __str__(self):
        return (
            f"{self.buyer.username} requested {self.quantity} of "
            f"'{self.submission.name}' from {self.seller.username} ({self.status})"
        )

# transactions/models.py
# transactions/models.py

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    submission = models.ForeignKey(FarmerSubmission, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    # Soft delete flags
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_receiver = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.content[:20]}"
