
from .models import ContactRequest
from accounts.models import CartItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import CartItem
from transactions.models import ContactRequest, Message

def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.info(request, "Your cart is empty.")
        return redirect('cart')

    if request.method == 'POST':
        for item in cart_items:
            # Create ContactRequest
            contact_request = ContactRequest.objects.create(
                buyer=request.user,
                seller=item.submission.user,
                submission=item.submission,
                quantity=item.quantity
            )
            
            # Create a Message tagged with the product
            content = (
                f"🛒 Request for '{item.submission.name}'\n"
                f"Quantity: {item.quantity}\n"
                f"Price per unit: MWK {item.submission.price:,}"
            )
            Message.objects.create(
                sender=request.user,
                receiver=item.submission.user,
                submission=item.submission,
                content=content
            )

        cart_items.delete()
        messages.success(request, "✅ Your request has been sent! Check your chats.")
        return redirect('chat_list')  # redirect to chat list

    total_price = sum(item.submission.price * item.quantity for item in cart_items)

    return render(request, 'transactions/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

from django.shortcuts import redirect, get_object_or_404
from .models import Message

def delete_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, sender=request.user)
    msg.delete()
    # Redirect back to the referring page (chat detail)
    return redirect(request.META.get('HTTP_REFERER', 'chat_list'))



# views.py
@login_required
def contact_requests_view(request):
    requests = ContactRequest.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'contact_requests.html', {'requests': requests})


from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.models import FarmerSubmission
from .models import ContactRequest

def chat_list(request):
    """
    Show all users the current user has made contact requests with.
    """
    # Get all unique sellers the current user has contacted
    contacts = ContactRequest.objects.filter(buyer=request.user).select_related('submission', 'seller').order_by('-created_at')

    context = {
        'contacts': contacts,
    }
    return render(request, 'transactions/chat_list.html', context)

# transactions/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Message, ContactRequest
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message

def chat_detail(request, seller_id):
    seller = get_object_or_404(User, id=seller_id)

    # Handle sending a new message
    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=seller,
                content=content
            )
        return redirect('chat_detail', seller_id=seller.id)

    # Only show messages not deleted by current user
    messages = Message.objects.filter(
        sender__in=[request.user, seller],
        receiver__in=[request.user, seller]
    ).exclude(
        (Q(sender=request.user) & Q(deleted_by_sender=True)) |
        (Q(receiver=request.user) & Q(deleted_by_receiver=True))
    ).order_by('timestamp')

    return render(request, 'transactions/chat_detail.html', {
        'seller': seller,
        'messages': messages
    })

def delete_chat(request, seller_id):
    seller = get_object_or_404(User, id=seller_id)

    # Soft-delete messages for the current user
    Message.objects.filter(
        sender=request.user, receiver=seller
    ).update(deleted_by_sender=True)

    Message.objects.filter(
        sender=seller, receiver=request.user
    ).update(deleted_by_receiver=True)

    return redirect('chat_list')
