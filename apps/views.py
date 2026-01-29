from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Brand, Car, RentCar
from .forms import RentCarForm


def home_page(request):
    """Bosh sahifa"""
    featured_cars = Car.objects.filter(is_featured=True, status='mavjud')[:6]
    new_cars = Car.objects.filter(status='mavjud').order_by('-created_at')[:6]
    brands = Brand.objects.all()[:10]
    
    context = {
        'featured_cars': featured_cars,
        'new_cars': new_cars,
        'brands': brands,
        'total_cars': Car.objects.filter(status='mavjud').count(),
    }
    return render(request, 'index.html', context)


def car_list(request):
    """Avtomobillar ro'yxati"""
    cars = Car.objects.filter(status='mavjud')
    brands = Brand.objects.all()
    
    # Filtrlash
    brand_id = request.GET.get('brand')
    search = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    fuel_type = request.GET.get('fuel_type')
    transmission = request.GET.get('transmission')
    
    if brand_id:
        cars = cars.filter(brand_id=brand_id)
    if search:
        cars = cars.filter(Q(name__icontains=search) | Q(brand__name__icontains=search))
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    if transmission:
        cars = cars.filter(transmission=transmission)
    
    # Pagination
    paginator = Paginator(cars, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'cars': page_obj,
        'brands': brands,
        'selected_brand': brand_id,
        'search': search,
        'min_price': min_price,
        'max_price': max_price,
        'fuel_type': fuel_type,
        'transmission': transmission,
    }
    return render(request, 'car.html', context)


def car_detail(request, car_id):
    """Avtomobil batafsil ma'lumotlari"""
    car = get_object_or_404(Car, id=car_id, status='mavjud')
    related_cars = Car.objects.filter(brand=car.brand, status='mavjud').exclude(id=car.id)[:4]
    
    if request.method == 'POST':
        form = RentCarForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.car = car
            rental.save()
            messages.success(request, 'Arizangiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog\'lanamiz.')
            return redirect('car_detail', car_id=car.id)
    else:
        form = RentCarForm()
    
    context = {
        'car': car,
        'related_cars': related_cars,
        'form': form,
    }
    return render(request, 'car-single.html', context)


def new_cars(request):
    """Yangi avtomobillar"""
    cars = Car.objects.filter(status='mavjud', year__gte=2023).order_by('-created_at')
    brands = Brand.objects.all()
    
    # Filtrlash
    brand_id = request.GET.get('brand')
    search = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if brand_id:
        cars = cars.filter(brand_id=brand_id)
    if search:
        cars = cars.filter(Q(name__icontains=search) | Q(brand__name__icontains=search))
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)
    
    paginator = Paginator(cars, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'cars': page_obj,
        'brands': brands,
        'selected_brand': brand_id,
        'search': search,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'new-cars.html', context)


def used_cars(request):
    """Ishlatilgan avtomobillar"""
    cars = Car.objects.filter(status='mavjud', year__lt=2023).order_by('-year')
    brands = Brand.objects.all()
    
    # Filtrlash
    brand_id = request.GET.get('brand')
    search = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if brand_id:
        cars = cars.filter(brand_id=brand_id)
    if search:
        cars = cars.filter(Q(name__icontains=search) | Q(brand__name__icontains=search))
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)
    
    paginator = Paginator(cars, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'cars': page_obj,
        'brands': brands,
        'selected_brand': brand_id,
        'search': search,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'used-cars.html', context)


def services(request):
    """Xizmatlar sahifasi"""
    return render(request, 'services.html')


def pricing(request):
    """Narxlar sahifasi"""
    cars = Car.objects.filter(status='mavjud').order_by('price_per_day')[:20]
    context = {
        'cars': cars,
    }
    return render(request, 'pricing.html', context)


def about(request):
    """Biz haqimizda sahifasi"""
    return render(request, 'about.html')


def contact(request):
    """Aloqa sahifasi"""
    if request.method == 'POST':
        messages.success(request, 'Xabaringiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog\'lanamiz.')
        return redirect('contact')
    return render(request, 'contact.html')


@login_required
def admin_dashboard(request):
    """Admin panel dashboard"""
    if not request.user.is_superuser:
        messages.error(request, 'Sizda bu sahifaga kirish huquqi yo\'q!')
        return redirect('home')
    
    pending_rentals = RentCar.objects.filter(status='pending').order_by('-created_at')
    approved_rentals = RentCar.objects.filter(status='approved').order_by('-created_at')[:10]
    total_rentals = RentCar.objects.count()
    total_cars = Car.objects.count()
    total_brands = Brand.objects.count()
    
    context = {
        'pending_rentals': pending_rentals,
        'approved_rentals': approved_rentals,
        'total_rentals': total_rentals,
        'total_cars': total_cars,
        'total_brands': total_brands,
    }
    return render(request, 'admin_dashboard.html', context)
