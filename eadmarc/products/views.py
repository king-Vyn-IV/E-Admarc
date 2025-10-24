from accounts.models import Product, FarmerSubmission

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Sum
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import intcomma

# Import your Order model

def sales_report(request):
    orders = Order.objects.all().order_by('-ordered_at')

    # Filters
    search = request.GET.get('search', '')
    status = request.GET.get('status', 'all')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if search:
        orders = orders.filter(product_name__icontains=search)

    if status != 'all':
        orders = orders.filter(status=status)

    if start_date:
        orders = orders.filter(ordered_at__date__gte=start_date)
    if end_date:
        orders = orders.filter(ordered_at__date__lte=end_date)

    # Total sales
    total_sales = orders.aggregate(total=Sum('total'))['total'] or 0

    # Pagination
    paginator = Paginator(orders, 5)  # 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders': page_obj.object_list,
        'total_sales': total_sales,
        'page_obj': page_obj,
    }
    return render(request, 'products/sales_report.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm

def manage_products(request):
    products = Product.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products:manage_products')
    else:
        form = ProductForm()

    context = {
        'products': products,
        'form': form,
    }
    return render(request, 'products/manage_products.html', context)


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:manage_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {'form': form, 'product': product})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('products:manage_products')

# products/views.py
from django.shortcuts import render
from .models import Product, FarmerSubmission


from django.core.serializers.json import DjangoJSONEncoder
import json

def market_trends_view(request):
    items = MarketItem.objects.prefetch_related('trends')
    market_data = []

    for item in items:
        trends = [{'date': t.date.strftime('%b %d'), 'price': float(t.price)} for t in item.trends.all().order_by('date')]
        market_data.append({
            'name': item.name,
            'trends': trends
        })

    context = {
        'market_data_json': json.dumps(market_data, cls=DjangoJSONEncoder)
    }
    return render(request, 'products/market_trends.html', context)



from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

def product_list(request):
    search_query = request.GET.get('q', '')
    filter_days = request.GET.get('filter')
    page_number = request.GET.get('page', 1)

    # Fetch all submissions, newest first
    submissions = FarmerSubmission.objects.all().order_by('-submitted_at')

    # Apply search filter
    if search_query:
        submissions = submissions.filter(name__icontains=search_query)

    # Apply date filter
    if filter_days:
        try:
            days = int(filter_days)
            since_date = timezone.now() - timedelta(days=days)
            submissions = submissions.filter(submitted_at__gte=since_date)
        except ValueError:
            pass

    # Pagination
    paginator = Paginator(submissions, 6)  # 6 submissions per page
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,  # template expects 'products'
        'request': request,
    }
    return render(request, 'products/product_list.html', context)


from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import Product  # your current app


@login_required
def approve_submission(request, submission_id):
    submission = get_object_or_404(FarmerSubmission, id=submission_id)
    submission.status = 'Approved'
    submission.save()
    messages.success(request, f'{submission.name} approved.')
    return redirect('product_list')  # use the correct URL name

@login_required
def reject_submission(request, submission_id):
    submission = get_object_or_404(FarmerSubmission, id=submission_id)
    submission.status = 'Rejected'
    submission.save()
    messages.error(request, f'{submission.name} rejected.')
    


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import FarmerSubmission  # Adjust if your model is elsewhere

@login_required
def add_product(request):
    if request.method == 'POST':
        form = FarmerSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.status = 'Pending'  # Default status
            submission.save()
            messages.success(request, '✅ Submission successful! Awaiting ADMARC review.')
            return redirect('add_product')  # Replace with your actual URL name
        else:
            messages.error(request, '❌ Submission failed. Please correct the errors below.')
    else:
        form = FarmerSubmissionForm()

    # Get submissions for the logged-in user, newest first
    submissions = FarmerSubmission.objects.filter(user=request.user).order_by('-submitted_at')

    return render(request, 'products/add_product.html', {
        'form': form,
        'submissions': submissions,
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import ProductSubmission

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if not name or not category or not quantity or not price:
            messages.error(request, "Please fill in all required fields.")
            return redirect("admin_addproduct")

        product = ProductSubmission.objects.create(
            user=request.user,
            name=name,
            category=category,
            quantity=quantity,
            price=price,
            description=description,
            image=image
        )
        messages.success(request, f"Product '{product.name}' uploaded successfully!")
        return redirect("admin_addproduct")

    submissions = ProductSubmission.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "products/admin_addproduct.html", {"submissions": submissions})

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProductSubmission

@login_required
def submission(request):
    """
    Display all draft submissions for the logged-in user in submission.html.
    Supports grid or list layout via 'view' GET parameter.
    """
    drafts = ProductSubmission.objects.filter(user=request.user).order_by('-created_at')

    # Choose layout: 'grid' or 'list'
    view_mode = request.GET.get('view', 'grid')  # default to grid

    context = {
        'drafts': drafts,
        'view_mode': view_mode,
    }
    return render(request, 'products/submission.html', context)


@login_required
def delete_submission(request, draft_id):
    draft = get_object_or_404(ProductSubmission, id=draft_id, user=request.user)
    if request.method == 'POST':
        draft.delete()
        messages.success(request, "Draft deleted successfully.")
    return redirect('submission')


@login_required
def edit_draft(request, draft_id):
    draft = get_object_or_404(ProductSubmission, id=draft_id, user=request.user, is_submitted=False)
    
    if request.method == 'POST':
        draft.name = request.POST.get('name')
        draft.category = request.POST.get('category')
        draft.quantity = request.POST.get('quantity')
        draft.price = request.POST.get('price')
        draft.description = request.POST.get('description')
        if request.FILES.get('image'):
            draft.image = request.FILES['image']
        draft.save()
        messages.success(request, "Draft updated successfully.")
        return redirect('submission')
    
    return render(request, 'products/edit_submission.html', {'draft': draft})
