from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Brand(models.Model):
    """Avtomobil brendlari"""
    name = models.CharField(max_length=100, verbose_name="Brend nomi")
    logo = models.ImageField(upload_to='brands/', blank=True, null=True, verbose_name="Logo")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    
    class Meta:
        verbose_name = "Brend"
        verbose_name_plural = "Brendlar"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Car(models.Model):
    """Avtomobillar"""
    FUEL_CHOICES = [
        ('benzin', 'Benzin'),
        ('dizel', 'Dizel'),
        ('elektro', 'Elektro'),
        ('gibrid', 'Gibrid'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('avtomat', 'Avtomat'),
        ('mexanik', 'Mexanik'),
        ('robot', 'Robot'),
    ]
    
    STATUS_CHOICES = [
        ('mavjud', 'Mavjud'),
        ('ijarada', 'Ijarada'),
        ('ta\'mirlanmoqda', 'Ta\'mirlanmoqda'),
    ]
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars', verbose_name="Brend")
    name = models.CharField(max_length=200, verbose_name="Model nomi")
    year = models.IntegerField(validators=[MinValueValidator(1900)], verbose_name="Ishlab chiqarilgan yil")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kunlik narx ($)")
    mileage = models.IntegerField(default=0, verbose_name="Yurgan masofa (km)")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='benzin', verbose_name="Yoqilg'i turi")
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='avtomat', verbose_name="Uzatmalar qutisi")
    seats = models.IntegerField(default=5, verbose_name="O'rindiqlar soni")
    color = models.CharField(max_length=50, verbose_name="Rang")
    image = models.ImageField(upload_to='cars/', default='cars/default.jpg', verbose_name="Rasm")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='mavjud', verbose_name="Holat")
    is_featured = models.BooleanField(default=False, verbose_name="Tavsiya etiladi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
    
    class Meta:
        verbose_name = "Avtomobil"
        verbose_name_plural = "Avtomobillar"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.year})"


class RentCar(models.Model):
    """Ijaraga olish arizalari"""
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlandi'),
        ('rejected', 'Rad etildi'),
        ('completed', 'Yakunlandi'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rentals', verbose_name="Avtomobil")
    full_name = models.CharField(max_length=200, verbose_name="To'liq ism")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    end_date = models.DateField(verbose_name="Tugash sanasi")
    total_days = models.IntegerField(default=1, verbose_name="Kunlar soni")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Jami narx ($)")
    message = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha xabar")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    admin_notes = models.TextField(blank=True, null=True, verbose_name="Admin eslatmalari")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
    
    class Meta:
        verbose_name = "Ijara arizasi"
        verbose_name_plural = "Ijara arizalari"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.car.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.total_days = delta.days + 1
            if self.car:
                self.total_price = self.car.price_per_day * self.total_days
        super().save(*args, **kwargs)
