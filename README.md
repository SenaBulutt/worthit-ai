# WorthIt AI

Yapay zeka destekli akıllı harcama analizi ve finansal karar destek sistemi.

## Proje Hakkında

WorthIt AI, kullanıcıların satın alma kararlarını gelir durumu, harcama tutarı, ihtiyaç durumu ve risk seviyesine göre analiz eden bir web uygulamasıdır.

Sistem;

- Harcama riski hesaplar
- WorthIt skoru üretir
- Finansal öneriler sunar
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

## Kurulum

```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## Ortam Değişkenleri

Projenin çalışması için `.env` dosyası oluşturulmalıdır.

Örnek:

```env
SECRET_KEY=your_secret_key
GROQ_API_KEY=your_api_key
