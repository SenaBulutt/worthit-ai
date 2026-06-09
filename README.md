# WorthIt AI

Yapay zeka destekli akıllı harcama analizi ve finansal karar destek sistemi.

## Proje Hakkında

WorthIt AI, kullanıcıların satın alma kararlarını gelir durumu, harcama tutarı, ihtiyaç durumu ve risk seviyesine göre analiz eden bir web uygulamasıdır.

Sistem;

- Harcama riski hesaplar
- WorthIt skoru üretir
- Finansal öneriler sunar
- E-posta doğrulamalı şifre sıfırlar
- Yapay zeka destekli yorum oluşturur
- Harcama hakkında soru-cevap desteği sağlar

## Kullanılan Teknolojiler

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap 5
- JavaScript
- Groq API (Llama 3.3 70B)
- Gmail SMTP

## Kurulum

```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## Ortam Değişkenleri

Projenin çalışması için proje kök dizininde `.env` dosyası oluşturulmalıdır.

```env
SECRET_KEY=your_secret_key_here
GROQ_API_KEY=your_groq_api_key_here
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
