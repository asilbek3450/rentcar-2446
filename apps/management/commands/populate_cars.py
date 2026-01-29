from django.core.management.base import BaseCommand
from apps.models import Brand, Car
import random


class Command(BaseCommand):
    help = '100 ta avtomobil yaratish (10 brend, har birida 10 ta)'

    def handle(self, *args, **options):
        # Brendlar ro'yxati
        brands_data = [
            {'name': 'Toyota', 'models': ['Camry', 'Corolla', 'RAV4', 'Land Cruiser', 'Highlander', 'Prius', 'Avalon', '4Runner', 'Sequoia', 'Tacoma']},
            {'name': 'Chevrolet', 'models': ['Malibu', 'Cruze', 'Equinox', 'Tahoe', 'Silverado', 'Traverse', 'Trax', 'Blazer', 'Suburban', 'Impala']},
            {'name': 'Hyundai', 'models': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Palisade', 'Kona', 'Venue', 'Accent', 'Veloster', 'Genesis']},
            {'name': 'Kia', 'models': ['Optima', 'Sorento', 'Sportage', 'Telluride', 'Forte', 'Rio', 'Soul', 'Stinger', 'Cadenza', 'Niro']},
            {'name': 'Mercedes-Benz', 'models': ['C-Class', 'E-Class', 'S-Class', 'GLE', 'GLC', 'GLS', 'A-Class', 'CLA', 'G-Class', 'AMG GT']},
            {'name': 'BMW', 'models': ['3 Series', '5 Series', '7 Series', 'X3', 'X5', 'X7', 'X1', 'X6', 'M3', 'M5']},
            {'name': 'Lexus', 'models': ['ES', 'LS', 'RX', 'NX', 'GX', 'LX', 'IS', 'RC', 'UX', 'LC']},
            {'name': 'Audi', 'models': ['A4', 'A6', 'A8', 'Q5', 'Q7', 'Q3', 'Q8', 'TT', 'R8', 'e-tron']},
            {'name': 'Ford', 'models': ['F-150', 'Explorer', 'Escape', 'Mustang', 'Edge', 'Expedition', 'Ranger', 'Bronco', 'Fusion', 'Focus']},
            {'name': 'Nissan', 'models': ['Altima', 'Sentra', 'Rogue', 'Pathfinder', 'Armada', 'Maxima', 'Murano', 'Frontier', 'Titan', 'Leaf']},
        ]

        fuel_types = ['benzin', 'dizel', 'benzin', 'benzin', 'dizel']  # Benzin ko'proq
        transmissions = ['avtomat', 'avtomat', 'mexanik', 'avtomat', 'robot']
        colors = ['Oq', 'Qora', 'Kumush', 'Qizil', 'Ko\'k', 'Kulrang', 'Jigarrang', 'Yashil']
        
        # Rasm fayllari ro'yxati (mavjud rasmlardan foydalanish)
        car_images = [
            'car-1.jpg', 'car-2.jpg', 'car-3.jpg', 'car-4.jpg', 'car-5.jpg',
            'car-6.jpg', 'car-7.jpg', 'car-8.jpg', 'car-9.jpg', 'car-10.jpg',
            'car-11.jpg', 'car-12.jpg'
        ]

        total_created = 0

        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(name=brand_data['name'])
            if created:
                self.stdout.write(self.style.SUCCESS(f'Brend yaratildi: {brand.name}'))
            
            for i, model_name in enumerate(brand_data['models']):
                # Har bir model uchun turli xil yillar va narxlar
                year = random.randint(2018, 2024)
                mileage = random.randint(0, 100000) if year < 2024 else random.randint(0, 50000)
                price_per_day = random.randint(20, 200)
                
                # Har bir brendning birinchi 3 ta modelini featured qilish
                is_featured = i < 3
                
                car, created = Car.objects.get_or_create(
                    brand=brand,
                    name=model_name,
                    defaults={
                        'year': year,
                        'price_per_day': price_per_day,
                        'mileage': mileage,
                        'fuel_type': random.choice(fuel_types),
                        'transmission': random.choice(transmissions),
                        'seats': random.choice([4, 5, 7, 8]),
                        'color': random.choice(colors),
                        'image': f'cars/{random.choice(car_images)}',
                        'description': f'{brand.name} {model_name} - {year} yil. Yuqori sifatli va qulay avtomobil.',
                        'status': 'mavjud',
                        'is_featured': is_featured,
                    }
                )
                
                if created:
                    total_created += 1
                    self.stdout.write(f'  ✓ {brand.name} {model_name} yaratildi')

        self.stdout.write(self.style.SUCCESS(f'\nJami {total_created} ta avtomobil yaratildi!'))
