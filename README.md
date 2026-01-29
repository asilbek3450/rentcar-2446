# RentCar - Avtomobil Ijaraga Olish Platformasi

Bu loyiha Django framework yordamida yaratilgan to'liq funksional avtomobil ijara platformasidir.

## Xususiyatlar

- ✅ 100 ta avtomobil (10 brend, har birida 10 ta model)
- ✅ Foydalanuvchilar avtomobil ma'lumotlarini ko'rish va ijara uchun ariza yuborish
- ✅ Admin panel orqali arizalarni boshqarish (tasdiqlash/rad etish)
- ✅ To'liq o'zbek tilida interfeys
- ✅ Qidiruv va filtrlash funksiyalari
- ✅ Responsive dizayn

## O'rnatish

1. Loyihani klon qiling yoki yuklab oling
2. Virtual environment yarating va faollashtiring:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows uchun: venv\Scripts\activate
```

3. Kerakli paketlarni o'rnating:
```bash
pip install django pillow
```

4. Ma'lumotlar bazasini yarating:
```bash
python3 manage.py migrate
```

5. Superuser yarating (asilbek/1234):
```bash
python3 manage.py create_superuser
```

6. Avtomobillarni yarating:
```bash
python3 manage.py populate_cars
```

7. Serverni ishga tushiring:
```bash
python3 manage.py runserver
```

## Foydalanish

### Foydalanuvchi uchun:
- Bosh sahifa: `http://127.0.0.1:8000/`
- Avtomobillar ro'yxati: `http://127.0.0.1:8000/avtomobillar/`
- Avtomobil batafsil: `http://127.0.0.1:8000/avtomobil/<id>/`

### Admin panel:
- URL: `http://127.0.0.1:8000/admin/`
- Login: `asilbek`
- Parol: `1234`

## Admin Panel Funksiyalari

1. **Brendlar boshqaruvi**: Yangi brendlar qo'shish, tahrirlash
2. **Avtomobillar boshqaruvi**: Avtomobillarni qo'shish, tahrirlash, o'chirish
3. **Ijara arizalari**: 
   - Kutilayotgan arizalarni ko'rish
   - Telefon raqamini ko'rib mijoz bilan bog'lanish
   - Arizalarni tasdiqlash yoki rad etish
   - Admin eslatmalari qo'shish

## Modellar

### Brand (Brend)
- name: Brend nomi
- logo: Brend logosi
- description: Tavsif

### Car (Avtomobil)
- brand: Brend (ForeignKey)
- name: Model nomi
- year: Yil
- price_per_day: Kunlik narx
- mileage: Yurgan masofa
- fuel_type: Yoqilg'i turi (benzin, dizel, elektro, gibrid)
- transmission: Uzatmalar qutisi (avtomat, mexanik, robot)
- seats: O'rindiqlar soni
- color: Rang
- image: Rasm
- status: Holat (mavjud, ijarada, ta'mirlanmoqda)
- is_featured: Tavsiya etiladi

### RentCar (Ijara arizasi)
- car: Avtomobil (ForeignKey)
- full_name: To'liq ism
- phone: Telefon raqami
- email: Email
- start_date: Boshlanish sanasi
- end_date: Tugash sanasi
- total_days: Kunlar soni (avtomatik hisoblanadi)
- total_price: Jami narx (avtomatik hisoblanadi)
- message: Qo'shimcha xabar
- status: Holat (pending, approved, rejected, completed)
- admin_notes: Admin eslatmalari

## Management Commands

### Avtomobillar yaratish:
```bash
python3 manage.py populate_cars
```

### Superuser yaratish:
```bash
python3 manage.py create_superuser
```

## Texnologiyalar

- Django 5.2.1
- SQLite (development)
- Bootstrap 4
- Font Awesome icons

## Muallif

MarsGroups - NB-2446

## Litsenziya

Bu loyiha shaxsiy loyiha sifatida yaratilgan.
# rentcar-2446
