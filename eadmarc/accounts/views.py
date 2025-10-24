from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CartItem  # Adjust to your cart model
from .models import Product  # Adjust path
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from .models import Submission  # ✅ correct impor
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from accounts.models import FarmerSubmission


# Helper function to check if user is admin
def is_admin(user):
    return user.is_superuser

from .forms import UserRegisterForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally log in user or redirect
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect('login')

# Define your admin check function
def is_admin(user):
    return user.is_staff or user.is_superuser  # Adjust according to your admin logic

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Dashboard statistics
    stats = [
        {
            'label': 'Pending Submissions',
            'value': 25,
            'icon': 'fa-regular fa-clock',
            'bg_color_start': '#fde68a',  # gradient start (yellow-200)
            'bg_color_end': '#f59e0b',    # gradient end (orange-500)
            'emoji': '⏳'
        },
        {
            'label': 'Total Orders',
            'value': 120,
            'icon': 'fa-solid fa-cart-shopping',
            'bg_color_start': '#bfdbfe',  # gradient start (blue-200)
            'bg_color_end': '#3b82f6',    # gradient end (blue-500)
            'emoji': '🛒'
        },
        {
            'label': 'Pending Orders',
            'value': 8,
            'icon': 'fa-solid fa-spinner',
            'bg_color_start': '#fef9c3',  # gradient start (yellow-100)
            'bg_color_end': '#facc15',    # gradient end (yellow-400)
            'emoji': '⏳'
        },
        {
            'label': 'Completed',
            'value': 97,
            'icon': 'fa-solid fa-circle-check',
            'bg_color_start': '#bbf7d0',  # gradient start (green-200)
            'bg_color_end': '#16a34a',    # gradient end (green-700)
            'emoji': '✅'
        },
        {
            'label': 'Total Revenue',
            'value': 'MWK 12,450,000',
            'icon': 'fa-solid fa-sack-dollar',
            'bg_color_start': '#e9d5ff',  # gradient start (purple-200)
            'bg_color_end': '#8b5cf6',    # gradient end (purple-500)
            'emoji': '💰'
        },
    ]

    # Quick action cards
    actions = [
        {
            'title': 'Manage Products',
            'description': 'View, add, edit or delete ADMARC products',
            'link': '#',
            'gradient': 'bg-gradient-to-br from-green-500 to-emerald-600',
            'icon': 'fa-solid fa-box'
        },
        {
            'title': 'Orders Management',
            'description': 'Track and manage all consumer orders',
            'link': '#',
            'gradient': 'bg-gradient-to-br from-blue-500 to-cyan-600',
            'icon': 'fa-solid fa-cart-shopping'
        },
        {
            'title': 'Sales Reports',
            'description': 'View sales data and generate reports',
            'link': '#',
            'gradient': 'bg-gradient-to-br from-purple-500 to-violet-600',
            'icon': 'fa-solid fa-chart-line'
        },
        {
            'title': 'Inventory Control',
            'description': 'Manage stock levels and availability',
            'link': '#',
            'gradient': 'bg-gradient-to-br from-orange-500 to-red-600',
            'icon': 'fa-solid fa-warehouse'
        },
        {
            'title': 'Search Marketplace',
            'description': 'Search products and orders quickly',
            'link': '#',
            'gradient': 'bg-gradient-to-br from-teal-500 to-cyan-600',
            'icon': 'fa-solid fa-magnifying-glass'
        },
    ]

    return render(request, 'accounts/admin_dashboard.html', {
        'title': 'Admin Dashboard',
        'stats': stats,
        'actions': actions,
    })

# Only allow superusers
def superuser_required(user):
    return user.is_superuser

@login_required
@user_passes_test(superuser_required)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'accounts/admin_users.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/add_user.html', {'form': form})

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm

def superuser_required(user):
    return user.is_superuser

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

@user_passes_test(superuser_required)
def edit_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        # ✅ Pass current_user so form can hide/show admin fields correctly
        form = UserRegisterForm(request.POST, instance=user_obj, current_user=request.user)

        if form.is_valid():
            updated_user = form.save(commit=False)

            # ✅ Only a superuser can change staff/superuser status
            if request.user.is_superuser:
                updated_user.is_superuser = form.cleaned_data.get('is_superuser', user_obj.is_superuser)
                updated_user.is_staff = form.cleaned_data.get('is_staff', user_obj.is_staff)
            else:
                # Prevent privilege escalation
                updated_user.is_superuser = user_obj.is_superuser
                updated_user.is_staff = user_obj.is_staff

            updated_user.save()

            messages.success(request, f"{updated_user.username}'s account was updated successfully!")
            return redirect('manage_users')
        else:
            messages.error(request, "There was an error updating the user. Please check the form.")
    else:
        # ✅ Include current_user for GET requests too
        form = UserRegisterForm(instance=user_obj, current_user=request.user)

    context = {
        'form': form,
        'user_obj': user_obj,
        'title': f"Edit User: {user_obj.username}",
    }
    return render(request, 'accounts/edit_user.html', context)

@login_required
@user_passes_test(superuser_required)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('manage_users')


@login_required
def users_dashboard(request):
    search_query = request.GET.get('q', '')
    filter_days = request.GET.get('filter')
    page_number = request.GET.get('page', 1)

    # Base querysets
    products = FarmerSubmission.objects.exclude(user=request.user)  # Exclude own submissions
    user_submissions = FarmerSubmission.objects.filter(user=request.user)

    # Apply search filter
    if search_query:
        products = products.filter(name__icontains=search_query)
        user_submissions = user_submissions.filter(name__icontains=search_query)

    # Apply date filter
    if filter_days:
        try:
            days = int(filter_days)
            since_date = timezone.now() - timedelta(days=days)
            products = products.filter(submitted_at__gte=since_date)
            user_submissions = user_submissions.filter(submitted_at__gte=since_date)
        except ValueError:
            pass

    # Order by descending submission date
    products = products.order_by('-submitted_at')
    user_submissions = user_submissions.order_by('-submitted_at')

    # Paginate products
    paginator = Paginator(products, 8)
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'user_submissions': user_submissions,
        'request': request,
    }

    return render(request, 'accounts/users_dashboard.html', context)


from django.shortcuts import render

def farmers_dashboard_view(request):
    # Mock market data
    market_data = [
        {
            "name": "Maize",
            "trends": [
                {"date": "Aug 1", "price": 150},
                {"date": "Aug 15", "price": 160},
                {"date": "Sep 1", "price": 170},
                {"date": "Sep 7", "price": 180},
            ],
        },
        {
            "name": "Rice",
            "trends": [
                {"date": "Aug 1", "price": 500},
                {"date": "Aug 15", "price": 520},
                {"date": "Sep 1", "price": 510},
                {"date": "Sep 7", "price": 530},
            ],
        },
    ]

    # Compute change and percentage for each item
    for item in market_data:
        earliest = item["trends"][0]["price"]
        latest = item["trends"][-1]["price"]
        item["change"] = latest - earliest
        item["change_percentage"] = round((item["change"] / earliest) * 100, 1)
        item["is_up"] = item["change"] > 0

    context = {
        "user": request.user,
        "total_products": 12,
        "total_earnings": 45600,
        "active_listings": 8,
        "customer_rating": "4.7/5",
        "market_data": market_data,
        "notifications_count": 3,
        "recent_activity": [
            {"title": "New product added:", "description": "Organic Tomatoes", "time_ago": "2 hours ago", "amount": "MWK 2,500/kg", "color": "success"},
            {"title": "Order received:", "description": "Sweet Potatoes (5kg)", "time_ago": "4 hours ago", "amount": "MWK 12,500", "color": "primary"},
        ],
        "messages": [
            {"sender": "Mary Phiri", "text": "Hi, is your maize still available?", "avatar": "images/user1.png"},
            {"sender": "John Banda", "text": "Can I get 10kg tomatoes?", "avatar": "images/user2.png"},
        ],
    }

    return render(request, "accounts/farmers_dashboard.html", context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FarmerSubmission
from products.forms import FarmerSubmissionForm  # make sure this exists

@login_required
def submission_edit(request, pk):
    submission = get_object_or_404(FarmerSubmission, pk=pk)

    # Ensure only the owner or admin can edit
    if submission.user != request.user and not request.user.is_superuser:
        messages.error(request, "You are not allowed to edit this submission.")
        return redirect('users_dashboard')

    if request.method == "POST":
        form = FarmerSubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, "Submission updated successfully!")
            return redirect('users_dashboard')
        else:
            messages.error(request, "Error updating the submission. Please check your form.")
    else:
        form = FarmerSubmissionForm(instance=submission)

    return render(request, 'accounts/edit_submission.html', {
        'form': form,
        'submission': submission
    })



def submission_delete(request, pk):
    submission = get_object_or_404(FarmerSubmission, pk=pk)
    if request.method == 'POST':
        submission.delete()
        return redirect('users_dashboard')  # ✅ Replace with the correct name of your dashboard URL
    return render(request, 'submissions/confirm_delete.html', {'submission': submission})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CartItem  # Update the import path based on your project structure

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CartItem

def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('submission')

    total = sum(item.submission.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'accounts/cart.html', context)


# accounts/views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import CartItem
from products.models import FarmerSubmission

def add_to_cart(request, submission_id):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect': '/accounts/login/'}, status=401)

    submission = get_object_or_404(FarmerSubmission, id=submission_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        submission=submission,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_count = CartItem.objects.filter(user=request.user).count()

    return JsonResponse({'success': True, 'cart_count': cart_count})


from django.shortcuts import redirect
from accounts.models import CartItem

def update_cart(request):
    if request.method == 'POST':
        # Update quantities
        for key, value in request.POST.items():
            if key.startswith('quantities_'):
                submission_id = key.split('_')[1]
                try:
                    cart_item = CartItem.objects.get(
                        user=request.user, 
                        submission_id=submission_id
                    )
                    new_quantity = int(value)
                    if new_quantity > 0:
                        cart_item.quantity = new_quantity
                        cart_item.save()
                    else:
                        cart_item.delete()  # Remove if quantity is 0
                except CartItem.DoesNotExist:
                    continue

        # Remove item if remove button was clicked
        remove_id = request.POST.get('remove')
        if remove_id:
            CartItem.objects.filter(user=request.user, submission_id=remove_id).delete()

    return redirect('cart')


# accounts/views.py
